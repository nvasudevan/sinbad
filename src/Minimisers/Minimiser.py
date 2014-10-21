import os
from sets import Set
import Lexer, CFG, Backends, Accent


class Minimiser:

    def __init__(self, ambimin):
        self.ambimin = ambimin
        self.tokenline = ""
        for l in open(self.ambimin.gf,'r'):
            if l.startswith('%token'):
                self.tokenline = l

        self.lex = Lexer.parse(open(self.ambimin.lf, "r").read())


    def find_ambiguity(self, gp, lp, duration):
        print "\n===> %s : %s" % (gp, self.ambimin.backend)
        self.cfg = CFG.parse(self.lex, open(gp, "r").read())
        self.parser = Accent.compile(gp, lp)
        bend = Backends.BACKENDS[self.ambimin.backend](self)
        return bend.run(self.ambimin.t_depth, self.ambimin.wgt, duration)


    def write_cfg(self, cfg, gp):
        gf = open(gp,'w')
        if self.tokenline != "":
            gf.write('%s\n\n' % self.tokenline) 
        gf.write('%nodefault\n\n')

        pp_seqs = Set()
        for seq in cfg['root']:
            seq_s = " ".join(str(e) for e in seq)
            pp_seqs.add(seq_s)

        gf.write("%s : %s\n;\n" % ('root', " | ".join(pp_seqs)))
        nt_list = [nt for nt in cfg.keys() if nt != 'root']
        nt_list.sort()
        for k in nt_list:
            pp_seqs = Set()
            for seq in cfg[k]:
                seq_s = " ".join(str(e) for e in seq)
                pp_seqs.add(seq_s)

            gf.write("%s : %s\n;\n" % (k," | ".join(pp_seqs)))
               
        gf.close() 


    def print_stats(self, gp, sen, is_amb, amb_subset):
        # number of rules, symbols, sentence length    
        cfg = CFG.parse(self.lex, open(gp, "r").read())
        no_rules = len(cfg.rules)
        no_seqs = 0
        no_symbols = 0 
        for rule in cfg.rules:
            no_seqs += len(rule.seqs)
            for seq in rule.seqs:
                no_symbols += len(seq)

        amb = ""
        len_amb_subset = ""
        if is_amb:
            amb = "yes" 
            assert amb_subset is not None
            len_amb_subset = len(amb_subset.split())

        out = "\nstats:%s, %s, %s, %s, %s, %s, %s" %  \
               (gp,amb,len(sen.split()),len_amb_subset,str(no_rules),str(no_seqs),str(no_symbols))
        print out 
    
