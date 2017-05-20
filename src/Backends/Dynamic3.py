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


import math, random, sys
import Accent, Backend, CFG, Utils



class Calc(Backend.Simple):
    def __init__(self, sin):
        Backend.Simple.__init__(self, sin)


    def next(self, depth, wgt=None):
        self._s = []
        self._depth = 0
        # the finite_depth part is reset at
        # every sentence generation
        for rule in self._cfg.rules:
            rule.finite_depth = None

        self._dive(self._cfg.get_rule(self._cfg.start_rulen), depth, wgt)

        # if whitespace exists, then join the token as is, otherwise join
        # with a space
        if "WS" in self._sin.lex.keys():
            return "".join(self._s)
        else:
            return " ".join(self._s)


    def _dive(self, rule, depth, wgt=None):
        self._depth += 1

        if self._depth > depth:
            # use seq with finite depth
            if rule.finite_depth is not None:
                seq = rule.finite_depth
            else:
                for _seq in rule.seqs:
                    _fd = True
                    for _e in _seq:
                        if isinstance(_e, CFG.Non_Term_Ref):
                            _ref_r = self._cfg.get_rule(_e.name)
                            if _ref_r.finite_depth == None:
                                _fd = False
                                break

                    if _fd:
                        rule.finite_depth = _seq
                        break;
                if rule.finite_depth is not None:
                    seq = rule.finite_depth
                else:
                    seq = random.choice(rule.seqs)

        else:
            seq = random.choice(rule.seqs)

        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                self._dive(self._cfg.get_rule(e.name), depth, wgt)
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        self._depth -= 1
