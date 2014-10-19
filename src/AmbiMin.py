#! /usr/bin/env python

import os, sys, tempfile, getopt, shutil
import Accent, Backends, CFG, Lexer
import AmbiParse 
import Minimisers

class AmbiMin:

    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1 : ], "hb:d:w:n:m:t:")
        self.gf,self.lf = None, None
        self.t_depth = None
        self.backend = None
        self.wgt = None
        self.mincnt = 0
        self.minimiser = None
        self.duration = None
        for opt in opts:
            if opt[0] == "-b":
                self.backend = opt[1]
            elif opt[0] == "-d":
                self.t_depth = int(opt[1])  
            elif opt[0] == "-w":
                self.wgt = float(opt[1])             
            elif opt[0] == "-n":
                self.mincnt = int(opt[1])
            elif opt[0] == "-m":
                self.minimiser = opt[1]
            elif opt[0] == "-t":
                self.duration = int(opt[1])
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

        if self.minimiser not in ['min1','min2']:
            self.usage("Don't understand minimisation method %s. Try min1 or min2" % self.minimiser)

        self.minimise_ambiguity()


    def usage(self, msg=None):
        if msg is not None:
            sys.stderr.write("\n%s\n" % msg)        
            sys.stderr.write("python AmbiMin.py -b <backend> -d <depth" \
                "-n <max minimisation count>" \
                "-w <wgt to apply on reaching threshold depth>" \
                "<grammar> <lex>")
            sys.exit(1)


    def minimise_ambiguity(self):
        min = Minimisers.MINIMISERS[self.minimiser](self)
        min.minimise()


AmbiMin()
