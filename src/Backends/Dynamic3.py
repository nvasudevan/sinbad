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

        for rule in self._cfg.rules:
            rule.entered = rule.exited = 0


    def next(self, depth, wgt):
        self._s = []
        self._depth = 0
        self.seqs_entered, self.seqs_exited = {},{}
        for rule in self._cfg.rules:
            self.seqs_entered[rule.name] = ([0] * len(rule.seqs))
            self.seqs_exited[rule.name] =  ([0] * len(rule.seqs))
                    
        self._dive(self._cfg.get_rule(self._cfg.start_rulen), depth, wgt)

        return " ".join(self._s)


    def _wtind(self, scores):
        total = sum(scores)
        rndscore = random.random() * total
        
        for i,sc in enumerate(scores):
            rndscore -= sc
            if rndscore <= 0:
                return i
                
                
    def _dive(self, rule, depth, wgt):
        self._depth += 1

        rule.entered += 1

        if self._depth > depth:
            # If we've exceeded the depth threshold, see if there are sequences
            # which only contain terminals, to ensure that we don't recurse any
            # further. If so, pick one of those randomly; otherwise, pick one of
            # the other sequences randomly.
            scores, wgtscores = [],[]
            for seq in rule.seqs:
                maxscore = 0
                for e in seq:
                    score = 0
                    if isinstance(e, CFG.Non_Term_Ref):
                        ref_rule = self._cfg.get_rule(e.name)
                        if ref_rule.entered == 0:
                            score = 0
                        else:
                            score = 1 - (ref_rule.exited * 1.0/ ref_rule.entered)
                    
                    if score > maxscore:
                        maxscore = score

                scores.append(maxscore)

            wgtscores = [(1-_sc) for _sc in scores]
            
            if random.random() < wgt:
                if sum(wgtscores) > 0:
                    i_seq = self._wtind(wgtscores)
                else:
                    i_seq = random.randrange(0,len(rule.seqs))
            else:
                minsc = min(scores)
                i_min_seqs = [] 
                for i in range(len(rule.seqs)):
                    if scores[i] == minsc:
                        i_min_seqs.append(i)
                
                i_seq = random.choice(i_min_seqs)
                
            seq = rule.seqs[i_seq]
            
        else:
            i_seq = random.randrange(0,len(rule.seqs))
            seq = rule.seqs[i_seq]

                
        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                self._dive(self._cfg.get_rule(e.name), depth, wgt)
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        rule.exited += 1
        
        self._depth -= 1