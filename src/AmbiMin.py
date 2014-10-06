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


    def minimise_ambiguity(self, gp, lp):
        tokenline = ""
        for l in open(gp,'r'):
            if l.startswith('%token'):
                tokenline = l
                
        is_amb, sen, acc_out = self.find_ambiguity(gp, lp)
        curramblen = len(sen)
        print "ambiguous sentence: %s [%s]" % (sen,curramblen)

        mincfg = AmbiParse.parse(self.cfg, acc_out) 
        # write the cfg and run ACCENT
        n = 1
        while n < 5: 
            new_gp = "%s.%s.acc" % (gp.split('.')[0],str(n))
            print "\n=> " , new_gp
            self.write_cfg(mincfg, new_gp, tokenline)
            is_amb, sen, acc_out = self.find_ambiguity(new_gp, lp)
            curramblen = len(sen)
            print "ambiguous sentence: %s [%s]" % (sen,curramblen)
            n += 1



AmbiMin()
