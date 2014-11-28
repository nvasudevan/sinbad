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


class Min1a(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def minimise(self):
        td = tempfile.mkdtemp()
        is_amb, sen, acc_out = self.find_ambiguity(self.ambimin.gf,
                                                   self.ambimin.lf,
                                                   None)
	assert is_amb
        ambi_parse = AmbiParse.parse(self, acc_out)
        min_cfg = ambi_parse.ambiguous_cfg_subset()
        amb_subset = ambi_parse.ambiguous_subset()
        min_gp = os.path.join(td,"0.acc")
        self.write_cfg(min_cfg, min_gp)

        cfg_size = self.cfg_size(min_cfg)
        print "stats:[0]:%s" % (cfg_size)
        i = 1
	n = 1
        currgp = min_gp
        while i <= 50: 
            is_amb, sen, acc_out = self.find_ambiguity(currgp, self.ambimin.lf, None)
            assert is_amb
            ambi_parse = AmbiParse.parse(self, acc_out)
            min_cfg = ambi_parse.ambiguous_cfg_subset()
            _cfg_size = self.cfg_size(min_cfg)
            print "stats:[%s]:%s" % (str(n),_cfg_size)
            if _cfg_size < cfg_size:
                # reset the counter
                i = 1
                amb_subset = ambi_parse.ambiguous_subset()
                min_gp = os.path.join(td,"%s.acc" % str(n))
                self.write_cfg(min_cfg, min_gp)
                currgp = min_gp
                cfg_size = _cfg_size
            else:
                i += 1

            n += 1

        if os.path.exists(td):
            shutil.rmtree(td)

