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
import Utils


class AmbiMin:

    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:], "hb:d:w:n:m:t:l:j:f:o:x:T:s")
        self.gp, self.lp = None, None
        self.t_depth = None
        self.backend = None
        self.wgt = None
        self.mincnt = 0
        self.minimiser = None
        self.duration = None
        self.ambi_duration = None
        self.save_min_cfg = False
        self.statslog = None
        self.ambijarp = None
        self.heap = None
        self.fltr = None
        self.fltr_cfg_outfmt = None

        if len(args) != 2:
            self.usage("grammar and lex is not set")

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
            elif opt[0] == "-T":
                self.ambi_duration = int(opt[1])
            elif opt[0] == "-s":
                self.save_min_cfg = True
            elif opt[0] == "-l":
                self.statslog = opt[1]
            elif opt[0] == "-j":
                self.ambijarp = opt[1]
            elif opt[0] == "-x":
                self.heap = opt[1]
            elif opt[0] == "-f":
                self.fltr = opt[1]
            elif opt[0] == "-o":
                self.fltr_cfg_outfmt = opt[1]
            elif opt[0] == "-h":
                self.usage()
            else:
                self.usage("Unknown argument '%s'" % opt[0])

        self.gp, self.lp = args[0], args[1]

        if self.backend is None:
            self.usage("** backend (-b <>) is not set **\n")

        if self.t_depth is None:
            self.usage("** depth (-d <>) is not set **\n")

        if self.statslog is None:
            self.usage("** stats log (-l <>) is not set **\n")

        self.minimise_ambiguity()


    def usage(self, msg=None):
        if msg is not None:
            sys.stderr.write("\n%s\n" % msg)
            sys.stderr.write("python AmbiMin.py [options] <grammar> <lex>\n\n")
            sys.stderr.write("Options include:\n"
                "   -m <minimiser type (min1|min2|..)>\n"
                "   -n <no of iterations for minimisation>\n"
                "   -b <backend>\n"
                "   -d <depth\n"
                "   -w <wgt to apply on reaching threshold depth>\n"
                "   -l <log to write stats to>\n"
                "   -s <save the minimised grammar with .<minimiser> extn>\n"
                "   -j <path to ambidexter jar file>\n"
                "   -T <duration to run ambidexter>\n"
                "   -x <heap size (1g|512m) for ambidexter>\n"
                "   -f <for ambidexter: filter (lr0|slr1|lalr1|lr1) to apply>\n"
                "   -o <output format for the filtered grammar>\n")

            sys.exit(1)


    def minimise_ambiguity(self):
        min = Minimisers.MINIMISERS[self.minimiser](self)
        min.minimise()


AmbiMin()
