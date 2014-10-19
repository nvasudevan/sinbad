import os, sys, tempfile, shutil
import Minimiser, AmbiParse
import CFG, Utils


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
        is_amb, sen, acc_out = self.find_ambiguity(self.ambimin.gf, self.ambimin.lf, None)
        assert is_amb
        mincfg = AmbiParse.parse(acc_out) 
        td = tempfile.mkdtemp()
        new_gp = os.path.join(td,"0.acc")
        self.write_cfg(mincfg, new_gp)
        Utils.print_stats(new_gp, self.ambimin.lf, sen, is_amb)
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
                        is_amb,sen,acc_out = self.find_ambiguity(new_gp, self.ambimin.lf, self.ambimin.duration)
                        Utils.print_stats(new_gp, self.ambimin.lf, sen, is_amb)
                        if is_amb:
                            currgp = new_gp
                            found = True
                            break

                if found:
                    break


        if os.path.exists(td):
            shutil.rmtree(td)

