#! /usr/bin/env python

import os, sys, tempfile
import Accent, Backends, CFG, Lexer
import AmbiParse 
import tempfile


class AmbiMin:

    def __init__(self):
        self.gf = sys.argv[1]
        self.lf = sys.argv[2]
        self.backend = sys.argv[3]
        self.t_depth = int(sys.argv[4])
        self.wgt = float(sys.argv[5])
        self.mincnt = int(sys.argv[6])
        print "wgt: %s" % self.wgt
        self.wgt = None
        self.minimise_ambiguity(self.gf, self.lf)


    def find_ambiguity(self, gp, lp):
        print "===> %s : %s" % (gp, self.backend)
        self.lex = Lexer.parse(open(lp, "r").read())
        self.cfg = CFG.parse(self.lex, open(gp, "r").read())
        self.parser = Accent.compile(gp, lp)
        bend = Backends.BACKENDS[self.backend](self)
        return bend.ambisen(self.t_depth, self.wgt)


    def write_cfg(self, cfg, gp, tokenline):
        gf = open(gp,'w')
        if tokenline != "":
            gf.write('%s\n\n' % tokenline) 
        gf.write('%nodefault\n\n')
        rhs = " | ". join(alt for alt in cfg['root'])
        gf.write("%s : %s\n;\n" % ('root', rhs))
        for k in (nt for nt in cfg.keys() if nt != 'root'):
            rhs = " | ". join(alt for alt in cfg[k])
            #print "%s: %s;" % (k, rhs)
            gf.write("%s : %s\n;\n" % (k, rhs))
               
        gf.close() 


    def print_stats(self, gp, sen):
        # number of rules, symbols, sentence length    
        cfg = CFG.parse(self.lex, open(gp, "r").read())
        no_rules = len(cfg.rules)
        no_seqs = 0
        no_symbols = 0 
        for rule in cfg.rules:
            no_seqs += len(rule.seqs)
            for seq in rule.seqs:
                no_symbols += len(seq)
                 
        print "ambiguous sentence: %s" % (sen)
        out =  "\nstats:%s, %s, %s, %s, %s" % (os.path.split(gp)[1],len(sen),str(no_rules),str(no_seqs),str(no_symbols))
        print out 


    def minimise_ambiguity(self, gp, lp):
        tokenline = ""
        for l in open(gp,'r'):
            if l.startswith('%token'):
                tokenline = l
                
        currgp = gp
        n = 1
        while n <= self.mincnt: 
            print "[%s]currgp: %s" % (str(n),currgp)
            is_amb, sen, acc_out = self.find_ambiguity(currgp, lp)
            assert is_amb
            mincfg = AmbiParse.parse(acc_out) 
            new_gp = "%s.%s.acc" % (currgp.split('.')[0],str(n))
            self.write_cfg(mincfg, new_gp, tokenline)
            self.print_stats(currgp, sen)
            currgp = new_gp
            n += 1



AmbiMin()
