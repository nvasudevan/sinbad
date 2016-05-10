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


import os, subprocess, tempfile, shutil, sys
import Minimiser, AmbiParse
import CFG, Lexer, Accent
import Utils, MiniUtils
import AmbiDexter


class Min5(Minimiser.Simple):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        if ambimin.ambijarp is None:
            ambimin.usage("** Need path to AmbiDexter jar file **\n")

        if ambimin.fltr is None:
            ambimin.usage('** Which filter to apply for AmbiDexter? **\n')

        if ambimin.fltr_cfg_outfmt is None:
            ambimin.usage('** What should be output format for filtered grammars? **\n')

        fltr = '-%s' % self.ambimin.fltr
        fltr_out = '-%s' % self.ambimin.fltr_cfg_outfmt
        opts = ['-q', '-h', fltr, fltr_out]
        self.ambidxt = AmbiDexter.AmbiDexter(self.ambimin.ambijarp, opts, self.lex_ws)


    def minimise(self):
        td = tempfile.mkdtemp()
        gp, lp = self.run(td)
        self.save_min_cfg(gp, lp)
        shutil.rmtree(td, True)


    def run(self, td):
        currgp, currlp = self.ambimin.gp, self.ambimin.lp
        n = 1

        while n <= self.ambimin.mincnt:
            amb, sen, trees = self.find_ambiguity(currgp, currlp)
            assert amb
            ambi_parse = AmbiParse.parse(self, trees)
            gp = os.path.join(td, "%s.acc" % n)
            lp = os.path.join(td, "%s.lex" % n)
            print "currgp: %s, gp: %s " % (currgp, gp)
            MiniUtils.write_cfg_lex(ambi_parse.min_cfg, gp, currlp, lp)
            self.write_stat(gp)

            currgp = gp
            currlp = lp
            n += 1

        # run ambidexter on the minimised grammar
        _gp = self.ambidxt.filter(currgp, str(self.ambimin.duration))
        self.write_stat(_gp)

        if _gp is not None:
            return _gp, currlp

        return currgp, currlp
