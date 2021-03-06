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
        if not self._sin.min_verify:
            if self._sin.td is None:
                self._sin.td = tempfile.mkdtemp()

            if not os.path.exists(self._sin.td):
                os.mkdir(self._sin.td)

            # write stats to the log for initial cfg and minimised cfg
            self.statslog = "%s/log" % self._sin.td
            open(self.statslog, "w").close()
            print "=> writing stats to %s" % self._sin.td
            self.write_stat(self._sin.gp, self._sin.lp)


    def run_accent(self, sen, gf, lf):
        """ build parser in td using gf+lf, and parse sentence sen."""

        parser = Accent.compile(gf, lf)
        ptrees = Accent.run(parser, sen)
        ambi_parse = AmbiParse.parse(lf, self._sin.lex_ws, ptrees, sen)
        #_gp = tempfile.mktemp('.acc', dir=self._sin.td)
        #_lp = tempfile.mktemp('.lex', dir=self._sin.td)
        #_ambstrp = os.path.join(self._sin.td, "%s.ambs" % 'accent')
        #self.write_cfg_lex(ambi_parse, _gp, _lp, _ambstrp)

        return ambi_parse


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
        # run ambidexter on the minimised grammar
        # from the sentence generated by ambidexter, pass it to accent
        # to generate final minimised grammar
        gp = self._sin.gp
        lp = self._sin.lp
        ambisen = self.ambidxt.ambiguous(gp, str(self._sin.ambit))
        if ambisen is None:
            # AmbiDexter didn't find anything
            self.write_stat(None, None, '-', '-')
            return gp, lp, None

        accsen = self.to_accent(ambisen, lp)
        print "ambisen: " , ambisen
        print "accsen: " , accsen

        _ambi_parse = self.run_accent(accsen, gp, lp)
        _gp = os.path.join(self._sin.td, "%s.acc" % 'ambidexter')
        _lp = os.path.join(self._sin.td, "%s.lex" % 'ambidexter')
        _senstrp = os.path.join(self._sin.td, "%s.sen" % 'ambidexter')
        _ambstrp = os.path.join(self._sin.td, "%s.ambs" % 'ambidexter')
        self.write_cfg_lex(_ambi_parse, _gp, _lp, _senstrp, _ambstrp)
        self.write_stat(_gp, _lp, _senstrp, _ambstrp)

        return _gp, _lp, _ambi_parse.amb_str
