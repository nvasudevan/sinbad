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


    def next(self, depth, wgt = None):
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


    def _dive(self, rule, depth, wgt):
        self._depth += 1
        #print "[%s]:: %s" % (self._depth, rule)

        if self._depth > depth:
            # use seq with finite depth
            if rule.finite_depth is not None:
                seq = rule.finite_depth
                #print "[fd:%s][%s]:: %s" % (self._depth, rule.finite_depth, rule)
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
                        #print "XXXXfd found: %s, %s" % (rule.finite_depth, rule)
                        #sys.exit(0)
                        break;
                if rule.finite_depth is not None:
                    seq = rule.finite_depth
                    #print "[fd:%s][%s]:: %s" % (self._depth, rule.finite_depth, rule)
                else:
                    seq = random.choice(rule.seqs)
                    #print "fd:rnd:[%s][%s]:: %s" % (self._depth, seq, rule)

        else:
            seq = random.choice(rule.seqs)

        # check for finite depth
        #if rule.finite_depth is None:
        #    finite_depth = True
        #    for e in seq:
        #        if isinstance(e, CFG.Non_Term_Ref):
        #            ref_r = self._cfg.get_rule(e.name)
        #            if ref_r.finite_depth == None:
        #                finite_depth = False
        #                break

        #    if finite_depth:
        #        rule.finite_depth = seq
        #        print "fd found: %s, %s" % (rule.finite_depth, rule)

        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                self._dive(self._cfg.get_rule(e.name), depth, wgt)
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        self._depth -= 1
