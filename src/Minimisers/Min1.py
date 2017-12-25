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


import os, tempfile
import CFG, Lexer
import Minimiser, AmbiParse


class Min1(Minimiser.Simple):

    def __init__(self, sin):
        Minimiser.Simple.__init__(self, sin)
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


    def run(self):
        currgp = self._sin.gp
        currlp = self._sin.lp
        currparse = None
        n = 1

        #while n < self._sin.mincnt:
        while True:
            amb, sen, ptrees = self._sin.find_ambiguity(currgp, currlp,
                                                      self._sin.backend)
            assert amb
            ambi_parse = AmbiParse.parse(currlp, self._sin.lex_ws, ptrees, sen)
            # save the minimised cfg, lex to target files
            _gp = os.path.join(self._sin.td, "%s.acc" % n)
            _lp = os.path.join(self._sin.td, "%s.lex" % n)
            _senstrp = os.path.join(self._sin.td, "%s.sen" % n)
            _ambstrp = os.path.join(self._sin.td, "%s.ambs" % n)
            print "currgp: %s, _gp: %s " % (currgp, _gp)
            self.write_cfg_lex(ambi_parse, _gp, _lp, _senstrp, _ambstrp)
            self.write_stat(_gp, _lp, _senstrp, _ambstrp)

            currgp = _gp
            currlp = _lp
            currparse = ambi_parse
            n += 1

        return currgp, currlp, currparse.amb_str
