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
import Minimiser, AmbiParse
import CFG
import Min2Utils

class Min2(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        self.symtokens = []
        if self.tokenline != "":
            tok_str = self.tokenline[7:len(self.tokenline)-1]
            self.sym_tokens = tok_str.replace(' ','').split(',')


    def pruned_cfg(self, gp):
        """ Given a grammar (gp), prune the unreachable rules."""

        cfg = CFG.parse(self.lex, open(gp, "r").read())
        unreachable = Min2Utils.unreachable_rules(cfg)
        if len(unreachable) > 0:
            print "=> unreachable: " , unreachable
            _cfg = {}
            for rule in cfg.rules:
                if rule.name not in unreachable:
                    _cfg[rule.name] = rule.seqs

            _dir, _gf = os.path.split(gp)
            _gp = os.path.join(_dir, "%s.%s" % ("pruned", _gf))
            self.write_cfg(_cfg, _gp)

            return _gp

        return gp


    def minimise(self, td):
        amb, sen, trees = self.find_ambiguity(self.ambimin.gp,
                                              self.ambimin.lp,
                                              None)
        assert amb
        ambi_parse = AmbiParse.parse(self, trees)
        self.add_stats(self.ambimin.gp, ambi_parse, sen)

        _gp = os.path.join(td, "0.acc")
        self.write_cfg(ambi_parse.min_cfg, _gp)

        currgp = _gp
        n = 1
        found = True
        while found:
            found = False
            cfg = CFG.parse(self.lex, open(currgp, "r").read())
            for rule in cfg.rules:
                if len(rule.seqs) > 1:
                    for i in range(len(rule.seqs)):
                        print "\n=> (%s) - %s" % (rule, rule.seqs[i])
                        min_cfg = Min2Utils.cfg_minus_alt(cfg, rule.name, i)
                        min_gp = os.path.join(td, "%s.acc" % n)
                        print "currgp: %s, min_gp: %s " % (currgp, min_gp)
                        self.write_cfg(min_cfg, min_gp)
                        n += 1

                        if Min2Utils.valid_cfg(min_gp, self.lex):
                            _gp = self.pruned_cfg(min_gp)
                            amb, sen, trees = self.find_ambiguity(_gp,
                                                         self.ambimin.lp,
                                                         self.ambimin.duration)
                            if amb:
                                ambi_parse = AmbiParse.parse(self, trees)
                                self.add_stats(_gp, ambi_parse, sen)
                                found = True
                                currgp = _gp
                                break

                if found:
                    break

        return currgp
