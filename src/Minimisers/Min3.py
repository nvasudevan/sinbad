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


import os, tempfile, shutil
import random
import Minimiser, AmbiParse
import CFG, Lexer
import MiniUtils


class Min3(Minimiser.Simple):

    def __init__(self, ambimin):
        Minimiser.Simple.__init__(self, ambimin)


    def rule_alts_combs(self, cfgmap):
        combs = []
        for k in cfgmap.keys():
            if len(cfgmap[k]) > 1:
                for i in range(len(cfgmap[k])):
                    combs.append((k, i))

        return combs


    def run(self):
        currgp = self._sin.mingp
        currlp = self._sin.minlp
        currparse = self._sin.ambi_parse
        n = 1
        found = True

        while found:
            found = False
            combs = self.rule_alts_combs(currparse.min_cfg)
            random.shuffle(combs)
            while combs:
                key, i = combs.pop()
                _cfg = MiniUtils.cfg_minus_alt(currparse.min_cfg, key, i)
                _gf, _lf = "%s.acc" % n, "%s.lex" % n
                _gp = os.path.join(self._sin.td, _gf)
                _lp = os.path.join(self._sin.td, _lf)
                MiniUtils.write_cfg_lex(_cfg, _gp, currlp, _lp)
                n += 1

                if MiniUtils.valid_cfg(_gp, _lp):
                    __gp, __lp = MiniUtils.pruned_cfg(_cfg, _gp, _lp)
                    amb, _, ptrees = self._sin.find_ambiguity(__gp, __lp,
                                       self._sin.backend, self._sin.mint)
                    if amb:
                        ambi_parse = AmbiParse.parse(self, ptrees)
                        _min_gp = os.path.join(self._sin.td, "min.%s" % _gf)
                        _min_lp = os.path.join(self._sin.td, "min.%s" % _lf)
                        MiniUtils.write_cfg_lex(ambi_parse.min_cfg,
                                                _min_gp, __lp, _min_lp)
                        self.write_stat(_min_gp, _min_lp)
                        found = True
                        currparse = ambi_parse
                        currgp = _min_gp
                        currlp = _min_lp
                        print "==> currp: %s " % currgp
                        break

        return currgp, currlp, currparse.amb_str
