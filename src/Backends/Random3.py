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


import math, random
import Accent, Backend, CFG, Utils



class Calc(Backend.Simple):
    def __init__(self, sin):
        Backend.Simple.__init__(self, sin)

        for rule in self._cfg.rules:
            rule.finite_depth = False

        # Calculate whether a given rule will definitely only recurse to a finite
        # depth. Note this doesn't mean it will only recurse 1 level: it may
        # recurse upto N levels, but there is a definite upper bound on N.
        #
        # Calculating this goes as follows. A rule whose sequences contain only
        # terminals is of finite depth. A rule whose sequences contain only
        # terminals or references to rules which are of finite depth is, itself,
        # of finite depth. Because of the latter rule, we iterate over all the
        # rules until we reach a fixed point.
        while 1:
            changed = False
            for rule in self._cfg.rules:
                if rule.finite_depth:
                    # If a rule is already known to be of finite depth, there's
                    # no point doing everything again.
                    continue

                for seq in rule.seqs:
                    finite_depth = True
                    for e in seq:
                        if isinstance(e, CFG.Non_Term_Ref):
                            ref_rule = self._cfg.get_rule(e.name)
                            if not ref_rule.finite_depth:
                                finite_depth = False
                                break
                    if not finite_depth:
                        break
                else:
                    rule.finite_depth = True
                    changed = True
            if not changed:
                break

        for rule in self._cfg.rules:
            rule.depth = 0


    def next(self, depth):
        self._s = []
        self._dive(self._cfg.get_rule(self._cfg.start_rulen), depth)

        return " ".join(self._s)


    def _dive(self, rule, depth):
        rule.depth += 1

        if rule.depth > depth:
            # If we've exceeded the depth threshold, see if there are sequences
            # which only contain terminals or finite depth non-terminals, to
            # ensure that we will only recurse a fixed number of times from this
            # point. If so, pick one of those randomly; otherwise, pick one of
            # the other sequences randomly.
            term_seqs = []
            for seq in rule.seqs:
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
                        ref_rule = self._cfg.get_rule(e.name)
                        if not ref_rule.finite_depth:
                            break
                else:
                    term_seqs.append(seq)

            if len(term_seqs) == 0:
                seq = random.choice(rule.seqs)
            else:
                seq = random.choice(term_seqs)
        else:
            seq = random.choice(rule.seqs)

        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                self._dive(self._cfg.get_rule(e.name), depth)
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        rule.depth -= 1
