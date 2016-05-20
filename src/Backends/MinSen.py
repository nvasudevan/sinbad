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

import CFG
import Utils


class Insert(object):

    def __init__(self, mincfg, minsen):
        self.subseq = mincfg.get_rule('root').seqs[0]
        print "Replacing %s with string %s" % (self.subseq, minsen)
        self.r, self.seqi, self.symi = Utils.find_rule(self._cfg, self.subseq)
        assert self.r is not None
        self.minsen = minsen
        self.found = False


    def insert_minsen(self, rule, depth, wgt=None):
        seq = rule.seqs[self.seqi]
        j = 0
        while j < len(seq):
            if (j < self.symi) or (j >= (self.symi+len(self.subseq))):
                e = seq[j]
                if isinstance(e, CFG.Non_Term_Ref):
                    self._dive(self._cfg.get_rule(e.name), depth, wgt)
                else:
                    self._s.append(self._cfg.gen_token(e.tok))
                j += 1
            else:
                self._s += [self.minsen]
                j += len(self.subseq) 

