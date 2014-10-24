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


import os, sys, tempfile, shutil
import Minimiser, AmbiParse
import CFG


class Min2(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        self.symtokens = []
        if self.tokenline != "":
            _tok_s = self.tokenline[7:len(self.tokenline)-1]
            self.symtokens = _tok_s.replace(' ','').split(',')


    def cfg_minus_alt(self, cfg, rule_name, i):
        _cfg = {}
        for rule in cfg.rules:
            rhs = []
            seqs = rule.seqs
            for j in range(len(seqs)):
                if not (rule.name == rule_name and j == i):
                    rhs.append(seqs[j]) 
                 
            _cfg[rule.name] = rhs

        return _cfg


    def minimise(self):
        td = tempfile.mkdtemp()
        is_amb, sen, acc_out = self.find_ambiguity(self.ambimin.gf, self.ambimin.lf, None)
        assert is_amb
        ambi_parse = AmbiParse.parse(self, acc_out) 
        mincfg = ambi_parse.min_cfg()
        amb_subset = ambi_parse.ambiguous_subset()
        new_gp = os.path.join(td,"0.acc")
        self.write_cfg(mincfg, new_gp)
        self.print_stats(new_gp, sen, is_amb, amb_subset)
        currgp = new_gp
        n = 1
        found = True
        while found:
            cfg = CFG.parse(self.lex, open(currgp, "r").read())
            found = False
            for rule in cfg.rules:
                if len(rule.seqs) > 1:
                    for i in range(len(rule.seqs)):
                        print "\n=> %s: %s" % (rule.name, rule.seqs[i])
                        new_cfg = self.cfg_minus_alt(cfg, rule.name, i)
                        new_gp = os.path.join(td, "%s.acc" % str(n))
                        n += 1
                        self.write_cfg(new_cfg, new_gp)
                        is_amb, sen, acc_out = self.find_ambiguity(new_gp, self.ambimin.lf, self.ambimin.duration)
                        if is_amb:
                            currgp = new_gp
                            found = True
                            ambi_parse = AmbiParse.parse(self, acc_out) 
                            amb_subset = ambi_parse.ambiguous_subset()
                            self.print_stats(new_gp, sen, is_amb, amb_subset)
                            break
                        else:
                            self.print_stats(new_gp, sen, is_amb, None)


                if found:
                    break


        if os.path.exists(td):
            shutil.rmtree(td)

