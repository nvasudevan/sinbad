#! /usr/bin/env python

import os, sys, tempfile, getopt
import Accent, Backends, CFG, Lexer
import AmbiParse 
import tempfile, shutil


class AmbiMin:

    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1 : ], "hb:d:w:n:")
        self.gf,self.lf = None, None
        self.t_depth = None
        self.backend = None
        self.wgt = None
        self.mincnt = None
        for opt in opts:
            if opt[0] == "-b":
                self.backend = opt[1]
            elif opt[0] == "-d":
                self.t_depth = int(opt[1])  
            elif opt[0] == "-w":
                self.wgt = float(opt[1])             
            elif opt[0] == "-n":
                self.mincnt = int(opt[1])
            elif opt[0] == "-h":
                self.usage()
            else:
                self.usage("Unknown argument '%s'" % opt[0])

        if len(args) != 2:
            self.usage()

        self.gf,self.lf = args[0],args[1]

        if self.backend is None:
            self.usage("backend is not set")

        if self.t_depth is None:
            self.usage("depth is not set")

        if self.mincnt is None:
            self.usage("minimisation count is not set")

        self.minimise_ambiguity(self.gf, self.lf)


    def usage(self, msg):
        if msg is not None:
            sys.stderr.write("\n%s\n" % msg)        
            sys.stderr.write("python AmbiMin.py -b <backend> -d <depth" \
                "-n <max minimisation count>" \
                "-w <wgt to apply on reaching threshold depth>" \
                "<grammar> <lex>")
            sys.exit(1)

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
        td = tempfile.mkdtemp()
        n = 1
        while n <= self.mincnt: 
            print "[%s]currgp: %s" % (str(n),currgp)
            is_amb, sen, acc_out = self.find_ambiguity(currgp, lp)
            assert is_amb
            mincfg = AmbiParse.parse(acc_out) 
            new_gp = os.path.join(td,"%s.acc" % str(n))
            self.write_cfg(mincfg, new_gp, tokenline)
            self.print_stats(currgp, sen)
            currgp = new_gp
            n += 1

#        if os.path.exists(td):
#            shutil.rmtree(td)


AmbiMin()
