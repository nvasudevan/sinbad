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
import CFG, Lexer
import MiniUtils


class Min2(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def minimise(self):
        td = tempfile.mkdtemp()
        gp, lp = self.run(td)
        # self.write_stats()
        self.save_min_cfg(gp, lp)
        # clean up
        shutil.rmtree(td, True)


    def run(self, td):
        currgp, currlp = self.ambimin.gp, self.ambimin.lp
        self.write_stat(currgp)
        amb, sen, trees = self.find_ambiguity(currgp, currlp, None)
        assert amb
        ambi_parse = AmbiParse.parse(self, trees)
        _gp, _lp = os.path.join(td, "0.acc"), os.path.join(td, "0.lex")
        MiniUtils.write_cfg_lex(ambi_parse.min_cfg, _gp, currlp, _lp)
        #self.add_stats(currgp, _gp, ambi_parse, sen)
        self.write_stat(_gp)

        currgp, currlp = _gp, _lp
        currcfg = ambi_parse.min_cfg
        n = 1
        found = True

        while found:
            found = False
            for key in currcfg.keys():
                seqs = currcfg[key]
                # Purging alt which are the only alt for a rule,
                # means we need to throw away the rule, and the rules
                # that refer to it - this will lead to mutating of
                # alternatives, and the modified grammar will become
                # unrecognisable from the original one.
                if len(seqs) > 1:
                    for i in range(len(seqs)):
                        _cfg = MiniUtils.cfg_minus_alt(currcfg, key, i)
                        _gf, _lf = "%s.acc" % n, "%s.lex" % n
                        _gp, _lp = os.path.join(td, _gf), os.path.join(td, _lf)
                        print "==> _gp: %s " % _gp
                        MiniUtils.write_cfg_lex(_cfg, _gp, currlp, _lp)
                        n += 1

                        if MiniUtils.valid_cfg(_gp, _lp):
                            __gp, __lp = MiniUtils.pruned_cfg(_cfg, _gp, _lp)
                            amb, sen, trees = self.find_ambiguity(__gp, __lp,
                                                       self.ambimin.duration)
                            if amb:
                                ambi_parse = AmbiParse.parse(self, trees)
                                # minimised gp usefule for stats
                                _min_gp = os.path.join(td, "min.%s" % _gf)
                                MiniUtils.write_cfg_lex(ambi_parse.min_cfg,
                                                        _min_gp, __lp)
                                # self.add_stats(__gp, _min_gp, ambi_parse, sen)
                                self.write_stat(_min_gp)
                                found = True
                                currcfg = _cfg
                                currgp = __gp
                                currlp = __lp
                                break

                if found:
                    break

        return currgp, currlp
