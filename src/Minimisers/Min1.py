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
import Minimiser, AmbiParse


class Min1(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def minimise(self):
        td = tempfile.mkdtemp()
        n = 1
        currgp = self.ambimin.gf
        while n <= self.ambimin.mincnt: 
            print "[%s]currgp: %s" % (str(n),currgp)
            is_amb, sen, acc_out = self.find_ambiguity(currgp, self.ambimin.lf, None)
            assert is_amb
            ambi_parse = AmbiParse.parse(self, acc_out)
            mincfg = ambi_parse.min_cfg()
            amb_subset = ambi_parse.ambiguous_subset()
            new_gp = os.path.join(td,"%s.acc" % str(n))
            self.write_cfg(mincfg, new_gp)
            self.print_stats(currgp, sen, is_amb, amb_subset)
            currgp = new_gp
            n += 1

        if os.path.exists(td):
            shutil.rmtree(td)

