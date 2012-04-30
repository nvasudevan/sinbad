#! /usr/bin/env python

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


import getopt, os, sys
import Accent, CFG, Fitness, Lexer


def find_ambiguity(gp, lp, ff_name):
    print "===> %s : %s" % (gp, ff_name)
    lex = Lexer.parse(open(lp, "r").read())
    cfg = CFG.parse(lex, open(gp, "r").read())
    parser = Accent.compile(gp, lp)
    ff_calc = Fitness.FITNESS_FUNCS[ff_name](cfg)
    while 1:
        s = ff_calc.next()
        out = Accent.run(parser, s)
        if Accent.was_ambiguous(out):
            print "Ambiguity found:\n"
            print "".join(out)
            return


def error(msg, c):
    sys.stderr.write(msg)
    sys.exit(c)


def check_file(p):
    if not os.path.isfile(p):
        sys.stderr.write("Can not read in %s\n" % p)
        sys.exit(1)


def usage(msg = None):

	if msg is not None:
		sys.stderr.write(msg + "\n\n")

	sys.stderr.write("sinbad -f <fitness function 1> [... -f <fitness function n>] <grammar 1> [... <grammar n>]\n")
	sys.exit(1)


def main():
    opts, args = getopt.getopt(sys.argv[1 : ], "hf:")
    fitnesses = []
    for opt in opts:
        if opt[0] == "-f":
            if opt[1] in fitnesses:
                usage("Fitness function '%s' specified more than once." % opt[1])
            if opt[1] not in Fitness.FITNESS_FUNCS:
                usage("Unknown fitness function '%s'." % opt[1])
            fitnesses.append(opt[1])
        elif opt[0] == "-h":
            usage()
        else:
            usage("Unknown argument '%s'" % opt[0])

    if len(fitnesses) == 0:
        usage("No fitness function specified.")
    if len(args) == 0:
        usage("Not enough arguments.")
    if len(args) % 2 != 0:
        usage("Some grammars are missing lexers.")

    i = 0
    while i < len(args):
        for fitness in fitnesses:
            check_file(args[i])
            check_file(args[i + 1])
            find_ambiguity(args[i], args[i + 1], fitness)
        i += 2



main()