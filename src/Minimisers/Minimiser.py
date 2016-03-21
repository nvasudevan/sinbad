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
        # write the initial cfg size
        self.write_stat(self.ambimin.gp)


    def find_ambiguity(self, gp, lp, duration=None):
        print "\n===> %s : %s" % (gp, self.ambimin.backend)
        self.cfg = CFG.parse(self.lex, open(gp, "r").read())
        self.parser = Accent.compile(gp, lp)
        bend = Backends.BACKENDS[self.ambimin.backend](self)
        return bend.run(self.ambimin.t_depth, self.ambimin.wgt, duration)


    def cfg_size(self, gp):
        _cfg = CFG.parse(self.lex, open(gp, "r").read())
        nrules = len(_cfg.rules)
        nalts, nsyms = 0, 0
        for r in _cfg.rules:
            nalts += len(r.seqs)
            for seq in r.seqs:
                nsyms += len(seq)

        return nrules, nalts, nsyms


    def save_min_cfg(self, gp, lp):
        if self.ambimin.save_min_cfg:
            gd, gf = os.path.split(self.ambimin.gp)
            gname, gext = os.path.splitext(gf)
            _gf = "%s.%s%s" % (gname, self.ambimin.minimiser, gext)
            min_gp = os.path.join(gd, _gf)
            ld, lf = os.path.split(self.ambimin.lp)
            lname, lext = os.path.splitext(lf)
            _lf = "%s.%s%s" % (lname, self.ambimin.minimiser, lext)
            min_lp = os.path.join(ld,  _lf)
            Utils.file_copy(gp, min_gp)
            Utils.file_copy(lp, min_lp)


    def write_stat(self, gp, tag=''):
        """ write no of rules, alts, symbols
            Use the tag to mark the final line
        """
        s = "-,-,-" 
        print "tag: " , tag
        if gp is not None:
            rules, alts, syms = self.cfg_size(gp)
            s = "%s,%s,%s" % (rules, alts, syms)

        with open(self.ambimin.statslog, "a") as logp:
            logp.write("%s%s\n" % (tag, s))
