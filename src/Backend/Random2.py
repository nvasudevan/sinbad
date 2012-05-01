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
import Accent, CFG, Utils



class Calc:
    def __init__(self, sin):
        self._sin = sin
        self._cfg = sin.cfg.clone()

        for rule in self._cfg.rules:
            rule.depth = 0


    def run(self):
        while 1:
            s = self.next()
            out = Accent.run(self._sin.parser, s)
            if Accent.was_ambiguous(out):
                print "Ambiguity found:\n"
                print "".join(out)
                return True


    def next(self):
        self._s = []
        while 1:
            self._dive(self._cfg.get_rule(self._cfg.start_rulen))

            if random.random() > 0.5:
                break

        return " ".join(self._s)


    def _dive(self, rule):
        rule.depth += 1

        if 1 - math.pow(math.e, -(random.randrange(rule.depth) / 2.5)) > 0.6:
            term_seqs = []
            for seq in rule.seqs:
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
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
                self._dive(self._cfg.get_rule(e.name))
            else:
                self._s.append(self._cfg.gen_token(e.tok))

        rule.depth -= 1