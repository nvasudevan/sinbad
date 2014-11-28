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


import os, subprocess, sys
from sets import Set
import Lexer, CFG, Backends, Accent
import Utils

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
            pp_seqs = [] # Set()
            for seq in cfg[k]:
                seq_s = " ".join(str(e) for e in seq)
                pp_seqs.append(seq_s)

            gf.write("%s : %s\n;\n" % (k," | ".join(pp_seqs)))
               
        gf.close() 

        if self.ambimin.save_min_cfg:
            #gp_d = os.path.split(self.ambimin.gf)[0]
            #gp_f = os.path.split(self.ambimin.gf)[1].split('.')[0]
            min_gp = "%s.%s.m" % (self.ambimin.gf,self.ambimin.minimiser)
            print "gp: %s, min_gp: %s" % (gp, min_gp)
            r = subprocess.call(["cp", gp, min_gp])
            if r != 0:
                Utils.error("Copy of %s -> %s failed!\n" % (gp, min_gp))

            print "Copied: %s -> %s\n" % (gp, min_gp)



    def cfg_size(self, cfg):
        size = 0
	for k in cfg.keys():
            seqs = cfg[k]
	    for seq in seqs:
                size += len(seq)

	return size


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
        len_sen = ""
        len_amb_subset = ""
        if is_amb:
            amb = "yes" 
            assert amb_subset is not None
            assert sen is not None
            len_sen = len(sen.split())
            len_amb_subset = len(amb_subset.split())

        out = "\nstats: %s, %s, %s, %s, %s, %s, %s" %  \
              (gp,amb, len_sen, len_amb_subset, str(no_rules), \
              str(no_seqs), str(no_symbols))
        print out 
    
