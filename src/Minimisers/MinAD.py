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
import CFG, Lexer
import Utils, MiniUtils


class MinAD(Minimiser.Simple):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def ambidexter(self, gp):
        cmd = ['./ambidexter.sh', gp, str(self.ambimin.duration)]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, _  = p.communicate()
        r = p.returncode
        # 0 - normal exit; 2 - ambiguous case
        if r != 0:
            msg = "AmbiDexter failed for %s (err: %s)\n" % (gp, r)
            return msg, r

        sen = out.split(':')[1]
        return sen, 0


    def minimise(self):
        td = tempfile.mkdtemp()
        gp, lp, sen = self.run(td)
        s = "summary: %s, %s, %s" % (self.cfg_size(self.ambimin.gp),
                                     self.cfg_size(gp), sen)

        print s
        self.save_min_cfg(gp, lp)
        # clean up
        shutil.rmtree(td, True)


    def run(self, td):
        gp, lp = self.ambimin.gp, self.ambimin.lp
        amb, sen, trees = self.find_ambiguity(gp, lp)
        assert amb
        ambi_parse = AmbiParse.parse(self, trees)
        # save the minimised cfg, lex to target files
        _gp = os.path.join(td, "%s.acc" % 0)
        _lp = os.path.join(td, "%s.lex" % 0)
        print "gp: %s, _gp: %s " % (gp, _gp)
        MiniUtils.write_cfg_lex(ambi_parse.min_cfg, _gp, lp, _lp)

        # run ambidexter on the minimised grammar
        sen, r = self.ambidexter(_gp)
        if r != 0:
            return _gp, _lp, None

        return _gp, _gp, sen
