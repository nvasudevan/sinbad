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


import os
import CFG
import Minimiser, AmbiParse, MiniUtils


class Min1(Minimiser.Simple):

    def __init__(self, sin):
        Minimiser.Simple.__init__(self, sin)
        if self._sin.mincnt is None:
            self._sin.usage("** Min1 requires no of iterations (-n N) **\n")


    def run(self):
        currgp = self._sin.mingp
        currlp = self._sin.minlp
        n = 1

        while n <= self._sin.mincnt:
            amb, sen, ptrees = self._sin.find_ambiguity(currgp, currlp,
                                                        self._sin.backend)
            assert amb
            ambi_parse = AmbiParse.parse(self, ptrees)
            # save the minimised cfg, lex to target files
            _gp = os.path.join(self._sin.td, "%s.acc" % n)
            _lp = os.path.join(self._sin.td, "%s.lex" % n)
            print "currgp: %s, _gp: %s " % (currgp, _gp)
            MiniUtils.write_cfg_lex(ambi_parse.min_cfg, _gp, currlp, _lp)
            self.write_stat(_gp, _lp)

            currgp = _gp
            currlp = _lp
            n += 1

        return currgp, currlp, ambi_parse.amb_str
