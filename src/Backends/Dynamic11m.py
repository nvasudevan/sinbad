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


import Dynamic11
import MinSen


class Calc(Dynamic11.Calc, MinSen.Insert):
    def __init__(self, sin, mincfg, minsen):
        Dynamic11.Calc.__init__(self, sin)
        MinSen.Insert.__init__(self, mincfg, minsen)


    def _dive(self, rule, depth, wgt):
        if (not self.found) and (rule.name == self.r): 
            self._depth += 1
            rule.entered += 1
            self.found = True
            print "found -> True"
            self.insert_minsen(rule, depth, wgt)
            rule.exited += 1
            self._depth -= 1
        else:
            Dynamic11.Calc._dive(self, rule, depth, wgt)

