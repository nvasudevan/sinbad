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
import CFG, Lexer
import Minimiser, AmbiParse


class Min2(Minimiser.Simple):

    def __init__(self, sin):
        Minimiser.Simple.__init__(self, sin)


    def run(self):
        currgp = self.mingp
        currlp = self.minlp
        currparse = self._sin.ambi_parse
        n = 1
        found = True

        while found:
            found = False
            lex = Lexer.parse(open(currlp, 'r').read())
            cfg = CFG.parse(lex, open(currgp, 'r').read())
            # work on rules with no of alts > 1
            keys = [r.name for r in cfg.rules if len(r.seqs) > 1]
            for key in keys:
                seqs = cfg.get_rule(key).seqs
                for i in range(len(seqs)):
                    _cfg = self.cfg_minus_alt(cfg, key, i)
                    if self.valid_cfg(_cfg):
                        # we could minimise lex first before pruning
                        _cfg_p = self.prune_cfg(_cfg, lex)
                        _gf, _lf = "%s.acc" % n, "%s.lex" % n
                        _gp = os.path.join(self._sin.td, "pruned.%s" % _gf)
                        CFG.write(_cfg_p, _gp)
                        n += 1
                        amb, _, ptrees = self._sin.find_ambiguity(_gp, currlp,
                                           self._sin.backend, self._sin.mint)
                        if amb:
                            ambi_parse = AmbiParse.parse(currlp, self._sin.lex_ws, ptrees)
                            __gp = os.path.join(self._sin.td, "min.%s" % _gf)
                            __lp = os.path.join(self._sin.td, "min.%s" % _lf)
                            self.write_cfg_lex(ambi_parse, __gp, __lp)
                            self.write_stat(__gp, __lp)
                            found = True
                            currparse = ambi_parse
                            currgp = __gp
                            currlp = __lp
                            break

                if found:
                    break

        return currgp, currlp, currparse.amb_str
