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


class Min4(Minimiser.Simple):

    def __init__(self, sin):
        Minimiser.Simple.__init__(self, sin)
        self.ambidxt = AmbiDexter.AmbiDexter(self._sin.ambijarp,
                                         ['-q', '-pg', '-ik', '0'],
                                         self._sin.jvmheap)


    def run_accent(self, sen, gp, lp):
        """ build parser in td using gp+lp, and parse sentence sen."""

        parser = Accent.compile(gp, lp)
        ptrees = Accent.run(parser, sen)
        ambi_parse = AmbiParse.parse(lp, self._sin.lex_ws, ptrees)
        _gp = tempfile.mktemp('.acc', dir=self._sin.td)
        _lp = tempfile.mktemp('.lex', dir=self._sin.td)
        self.write_cfg_lex(ambi_parse, _gp, _lp)

        return _gp, _lp, ambi_parse


    def to_accent(self, sen, lp):
        """ sen contains symbolic tokens, convert to 'actual' tokens using
            the lex
        """
        lex = Lexer.parse(open(lp, "r").read())
        _sen = []
        for tok in sen.split():
            if tok in lex.keys():
                _sen.append(lex[tok])
            else:
                # single char quoted tokens
                _sen.append(tok.replace("'", ""))

        if not self._sin.lex_ws:
            return " ".join(_sen)

        return "".join(_sen)


    def run(self):
        currgp = self.mingp
        currlp = self.minlp
        currparse = self._sin.ambi_parse
        n = 1

        while n <= self._sin.mincnt:
            amb, sen, ptrees = self._sin.find_ambiguity(currgp, currlp,
                                                        self._sin.backend)
            assert amb
            ambi_parse = AmbiParse.parse(currlp, self._sin.lex_ws, ptrees)
            # save the minimised cfg, lex to target files
            _gp = os.path.join(self._sin.td, "%s.acc" % n)
            _lp = os.path.join(self._sin.td, "%s.lex" % n)
            print "currgp: %s, _gp: %s " % (currgp, _gp)
            self.write_cfg_lex(ambi_parse, _gp, _lp)
            self.write_stat(_gp, _lp)

            currgp = _gp
            currlp = _lp
            currparse = ambi_parse
            n += 1

        # run ambidexter on the minimised grammar
        ambisen = self.ambidxt.ambiguous(currgp, str(self._sin.ambit))
        if ambisen is not None:
            accsen = self.to_accent(ambisen, currlp)
            print "ambisen: " , ambisen
            print "accsen: " , accsen
            # pass the string from ambidexter to accent,
            # to minimise the grammar even further
            _gp, _lp, _ambip = self.run_accent(accsen, currgp, currlp)
            self.write_stat(_gp, _lp, '*')
            return _gp, _lp, _ambip.amb_str

        # AmbiDexter didn't find anything
        self.write_stat(None, None, '*')
        return currgp, currlp, ambi_parse.amb_str
