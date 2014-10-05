#! /usr/bin/env python

import datetime, getopt, os, sys
import Accent, Backends, CFG, Lexer
import AmbiParse 
import re


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


                

    def minimise_ambiguity(self, gp, lp):
        is_amb, sen, acc_out = self.find_ambiguity(gp, lp)
        curramblen = len(sen)
        print "ambiguous sentence: %s [%s]" % (sen,curramblen)

        mincfg = AmbiParse.parse(self.cfg, acc_out) 


AmbiMin()
