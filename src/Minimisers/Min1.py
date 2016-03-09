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
import CFG
import Minimiser, AmbiParse, MiniUtils


class Min1(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        if ambimin.mincnt is None:
            ambimin.usage("** Need no of iterations for minimisation **\n")


    def minimise(self):
        td = tempfile.mkdtemp()
        gp, lp = self.run(td)
        #self.write_stats()
        self.save_min_cfg(gp, lp)
        # clean up
        shutil.rmtree(td, True)


    def run(self, td):
        """ Minimises a given CFG and return the final version
            of target cfg and lex
        """
        currgp = self.ambimin.gp
        currlp = self.ambimin.lp
        n = 1

        self.write_stat(currgp)
        while n <= self.ambimin.mincnt:
            amb, sen, trees = self.find_ambiguity(currgp, currlp, None)
            assert amb
            ambi_parse = AmbiParse.parse(self, trees)
            # save the minimised cfg, lex to target files
            _gp = os.path.join(td, "%s.acc" % n)
            _lp = os.path.join(td, "%s.lex" % n)
            print "currgp: %s, _gp: %s " % (currgp, _gp)
            MiniUtils.write_cfg_lex(ambi_parse.min_cfg, _gp, currlp, _lp)
            # add stats
            # self.add_stats(currgp, _gp, ambi_parse, sen)
            self.write_stat(_gp)

            currgp = _gp
            currlp = _lp
            n += 1

        return currgp, currlp
