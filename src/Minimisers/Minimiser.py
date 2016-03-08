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


import os, sys
import Lexer, CFG, Backends, Accent
import AmbiParse
import Utils


class Minimiser:

    def __init__(self, ambimin):
        self.ambimin = ambimin
        self.symtokens = []

        # keep note of symbolic tokens
        for l in open(self.ambimin.gp, 'r'):
            if l.startswith('%token'):
                token_line = l
                tok_str = token_line[7:len(token_line)-2]
                self.sym_tokens = tok_str.replace(' ', '').split(',')

        self.lex = Lexer.parse(open(self.ambimin.lp, "r").read())
        self.lex_ws = False
        if "WS" in self.lex.keys():
            self.lex_ws = True

        self.cfg_min_stats = []
        open(self.ambimin.statslog, "w").close()


    def find_ambiguity(self, gp, lp, duration=None):
        print "\n===> %s : %s" % (gp, self.ambimin.backend)
        self.cfg = CFG.parse(self.lex, open(gp, "r").read())
        self.parser = Accent.compile(gp, lp)
        bend = Backends.BACKENDS[self.ambimin.backend](self)
        return bend.run(self.ambimin.t_depth, self.ambimin.wgt, duration)


    def cfg_size(self, gp):
        _cfg = CFG.parse(self.lex, open(gp, "r").read())
        size = 0
        for r in _cfg.rules:
            for seq in r.seqs:
                size += len(seq)

        return size


    def save_min_cfg(self, gp, lp):
        if self.ambimin.save_min_cfg:
            min_gp = "%s.%s" % (self.ambimin.gp, self.ambimin.minimiser)
            min_lp = "%s.%s" % (self.ambimin.lp, self.ambimin.minimiser)
            Utils.file_copy(gp, min_gp)
            Utils.file_copy(lp, min_lp)


    def add_stats(self, initg, finalg, ambi_parse, sen):
        stats = (self.cfg_size(initg), self.cfg_size(finalg),
                 len(sen.split()), len(ambi_parse.amb_str.split()),
                 ambi_parse.amb_type)
        self.cfg_min_stats.append(stats)


    def write_stat(self, gp):
        with open(self.ambimin.statslog, "a") as logp:
            logp.write("%s," % self.cfg_size(gp))


    def _write_stats(self):
        print "\nstats: "
        for (gsize, tgsize, senl, ambl, ambtype) in self.cfg_min_stats:
            print "%s -> %s, %s, %s, %s" % (gsize, tgsize, senl, ambl, ambtype)

        i_gsize, i_tgsize, i_senl, i_ambl, i_type = self.cfg_min_stats[0]
        f_gsize, f_tgsize, f_senl, f_ambl, f_type = self.cfg_min_stats[-1]
        print "summary:%s,%s,,%s,%s,,%s,%s,,%s,%s" % (i_gsize, f_tgsize,
                                                      i_senl, f_senl,
                                                      i_ambl, f_ambl,
                                                      i_type, f_type)


