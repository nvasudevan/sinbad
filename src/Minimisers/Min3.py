# Copyright (c) 2012 King's College London
# created by Laurence Tratt and Naveneetha Vasudevan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


import os, subprocess, tempfile, shutil, sys
import Minimiser, AmbiParse
import CFG, Lexer, Accent
import Utils, MiniUtils
import AmbiDexter


class Min3(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        if ambimin.ambijarp is None:
            ambimin.usage("** Need path to AmbiDexter jar file **\n")


    def convert_sen(self, sen, lex):
        """ sen contains symbolic tokens, convert to 'actual' tokens."""
        _sen = []
        for tok in sen.split():
            if tok in lex.keys():
                _sen.append(lex[tok])
            else:
                # single char quoted tokens
                _sen.append(tok.replace("'", ""))

        if "WS" in lex.keys():
            return "".join(_sen)
        else:
            # the origingal grammar had WS rule but not anymore.
            if self.lex_ws:
                return "".join(_sen)

            return " ".join(_sen)


    def accent(self, sen, gp, lp, td):
        """ build parser in td using gp+lp, and parse sentence sen."""

        lex = Lexer.parse(open(lp, "r").read())
        _sen = self.convert_sen(sen, lex)
        parser = Accent.compile(gp, lp)
        print "sen (from ambi): " , sen
        print "sen (tokenised): **%s**" % _sen
        out = Accent.run(parser, _sen)
        ambiparse = AmbiParse.parse(self, out)
        _gp = os.path.join(td, "%s.acc" % 1)
        _lp = os.path.join(td, "%s.lex" % 1)
        MiniUtils.write_cfg_lex(ambiparse.min_cfg, _gp, lp, _lp)

        return _gp, _lp


    def minimise(self):
        td = tempfile.mkdtemp()
        gp, lp = self.run(td)
        self.save_min_cfg(gp, lp)
        shutil.rmtree(td, True)


    def run(self, td):
        currgp, currlp = self.ambimin.gp, self.ambimin.lp
        n = 1

        self.write_stat(currgp)
        while n <= self.ambimin.mincnt:
            amb, sen, trees = self.find_ambiguity(currgp, currlp)
            assert amb
            ambi_parse = AmbiParse.parse(self, trees)
            _gp = os.path.join(td, "%s.acc" % n)
            _lp = os.path.join(td, "%s.lex" % n)
            print "currgp: %s, _gp: %s " % (currgp, _gp)
            MiniUtils.write_cfg_lex(ambi_parse.min_cfg, _gp, currlp, _lp)
            self.write_stat(_gp)

            currgp = _gp
            currlp = _lp
            n += 1

        # run ambidexter on the minimised grammar
        opts = ['-q', '-pg', '-ik', '0']
        sen, r = AmbiDexter.ambiguous(currgp, self.ambimin.ambijarp,
                                      opts, str(self.ambimin.duration))
        if r == 0:
            # pass the string from ambidexter to accent,
            # to minimisei the grammar even further
            _gp, _lp = self.accent(sen, currgp, currlp, td)
            self.write_stat(_gp)
            return _gp, _lp

        return currgp, currlp
