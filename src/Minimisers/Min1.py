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


import os, tempfile
import CFG
import Minimiser, AmbiParse


class Min1(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def minimise(self, td):
        """ Minimises a given CFG and return the final version """
        n = 1
        currgp = self.ambimin.gp

        while n <= self.ambimin.mincnt: 
            #print "[%s]currgp: %s" % (n, currgp)
            is_amb, sen, parse_trees = self.find_ambiguity(currgp, self.ambimin.lp, None)
            assert is_amb
            ambi_parse = AmbiParse.parse(self, parse_trees)
            # extract the minimised cfg
            min_cfg = ambi_parse.ambiguous_cfg_subset()
            # extract the ambiguous string from sentence
            amb_str = ambi_parse.ambiguous_subset()

            # cfg size, sentence size, ambiguous string size, amb type
            ambi_type = "h"
            if ambi_parse.vamb:
                ambi_type = "v"

            stats = (self.cfg_size(currgp), len(sen.split()),
                     len(amb_str.split()), ambi_type)
            self.cfg_min_stats.append(stats)

            # write the min cfg to a temp file, reset currgp
            min_gp = os.path.join(td, "%s.acc" % n)
            self.write_cfg(min_cfg, min_gp)
            currgp = min_gp
            n += 1

        return currgp

