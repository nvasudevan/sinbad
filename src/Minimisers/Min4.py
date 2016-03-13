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
import tempfile
import Minimiser, AmbiParse
import CFG, Lexer, Accent
import Utils, MiniUtils
import AmbiDexter


class Min4(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        if ambimin.ambijarp is None:
            ambimin.usage("** Need path to AmbiDexter jar file **\n")


    def run_accent(self, sen, gp, lp, td):
        """ build parser in td using gp+lp, and parse sentence sen."""

        parser = Accent.compile(gp, lp)
        out = Accent.run(parser, sen)
        ambiparse = AmbiParse.parse(self, out)
        _gp = tempfile.mktemp('.acc', dir=td)
        _lp = tempfile.mktemp('.lex', dir=td)
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

        while n <= self.ambimin.mincnt:
            amb, sen, trees = self.find_ambiguity(currgp, currlp)
            assert amb
            ambi_parse = AmbiParse.parse(self, trees)
            gp = os.path.join(td, "%s.acc" % n)
            lp = os.path.join(td, "%s.lex" % n)
            print "currgp: %s, gp: %s " % (currgp, gp)
            MiniUtils.write_cfg_lex(ambi_parse.min_cfg, gp, currlp, lp)
            self.write_stat(gp)

            currgp = gp
            currlp = lp
            n += 1

        # run ambidexter on the minimised grammar
        opts = ['-q', '-pg', '-ik', '0']
        sen = AmbiDexter.ambiguous(currgp, self.ambimin.ambijarp,
                                   opts, str(self.ambimin.duration))
        if sen is not None:
            # pass the string from ambidexter to accent,
            # to minimisei the grammar even further
            _sen = MiniUtils.convert_sen(sen, currlp, self.lex_ws)
            _gp, _lp = self.run_accent(_sen, currgp, currlp, td)
            self.write_stat(_gp)
            return _gp, _lp

        # AmbiDexter didn't find anything
        self.write_stat(None)
        return currgp, currlp
