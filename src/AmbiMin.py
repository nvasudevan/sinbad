#! /usr/bin/env python
#
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


import os, sys, getopt
import Minimisers

class AmbiMin:

    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1 : ], "hb:d:w:n:m:t:s")
        self.gf,self.lf = None, None
        self.t_depth = None
        self.backend = None
        self.wgt = None
        self.mincnt = 0
        self.minimiser = None
        self.duration = None
        self.save_min_cfg = False

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
            elif opt[0] == "-s":
                self.save_min_cfg = True
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
