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
import Accent, Backend, CFG, Utils, sets


class Calc(Backend.Simple):
    def __init__(self, sin):
        Backend.Simple.__init__(self, sin)
        rules, self.terminating_indices,rules_to_remove = {}, {}, []
        
        # first identify terminal-only sequences
        for rule in self._cfg.rules:
            rule_seqs = []
            for ind,seq in enumerate(rule.seqs):
                _seq = []
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
                        _seq.append(e.name)
                if len(_seq) == 0:
                    if not self.terminating_indices.__contains__(rule.name):
                        self.terminating_indices[rule.name] = ind
                        rules_to_remove.append(rule.name)
                rule_seqs.append(_seq)
            if not self.terminating_indices.__contains__(rule.name):
                rules[rule.name] = rule_seqs

        while len(rules_to_remove) > 0:
            rules_to_remove = []
            for key in rules.keys():
                rule_seqs = []
                for ind,seq in enumerate(rules[key]):
                    _seq = []
                    for e in seq:
                        if e not in self.terminating_indices.keys():
                            _seq.append(e)
                    if len(_seq)== 0:
                        self.terminating_indices[key] = ind
                        rules_to_remove.append(key)
                        break
                    rule_seqs.append(_seq)
                    
                rules[key] = rule_seqs # if key not in self.terminating_indices.keys(), and remove the del lines below

            for del_key in rules_to_remove:
                del rules[del_key]
            

    def next(self, depth, wgt = None):
        self._s = []
        self._depth = 0
        self._dive(self._cfg.get_rule(self._cfg.start_rulen), depth)

        return " ".join(self._s)


    def _dive(self, rule, depth):
        self._depth += 1

        if self._depth > depth:
            # On exceeding the depth threshold, favour alternatives
            seq = rule.seqs[self.terminating_indices[rule.name]]
        else:
            seq = random.choice(rule.seqs)

        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                self._dive(self._cfg.get_rule(e.name), depth)
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        self._depth -= 1
