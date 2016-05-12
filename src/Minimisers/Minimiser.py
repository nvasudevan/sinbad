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


class Simple:

    def __init__(self, sin):
        self._sin = sin
        self.statslog = "%s/log" % self._sin.td
        open(self.statslog, "w").close()
        print "=> writing stats to %s" % self._sin.td
        self.write_stat(self._sin.gp, self._sin.lp)
        self.write_stat(self._sin.mingp, self._sin.minlp)
        self.symtokens = []

        # keep note of symbolic tokens
        for l in open(self._sin.mingp, 'r'):
            if l.startswith('%token'):
                token_line = l
                tok_str = token_line[7:len(token_line)-2]
                self.sym_tokens = tok_str.replace(' ', '').split(',')

        self.cfg_min_stats = []


    def minimise(self):
        """ Minimises a given CFG and return the final version
            of target cfg and lex
        """
        gp, lp, ambstr = self.run()
        print "ambstr: " , ambstr
        if self._sin.save_min_cfg:
            self.save_min_cfg(gp, lp)

        print "stats: %s\n" % (open(self.statslog, 'r').read())

        # verify the minimised sentence
        if self._sin.verify:
            r = self.verify_ambiguity(gp, lp, ambstr)
            if r:
                print "** minimisation with %s verified **" % self._sin.minp


    def verify_ambiguity(self, mingp, minlp, minsen, duration=None):
        print "\n===> [verify] %s : %s" % (self._sin.gp, self._sin.backend)
        self._sin.lex = Lexer.parse(open(self._sin.lp, 'r').read())
        self._sin.cfg = CFG.parse(self._sin.lex, open(self._sin.gp, "r").read())
        self._sin.parser = Accent.compile(self._sin.gp, self._sin.lp)

        minlex = Lexer.parse(open(minlp, 'r').read())
        mincfg = CFG.parse(minlex, open(mingp, 'r').read())
        seq = mincfg.get_rule('root').seqs[0]
        # check if the root rule of minimised cfg == root of original cfg
        if (len(seq) == 1) and (str(seq[0]) == self._sin.cfg.start_rulen):
            out = Accent.run(self._sin.parser, minsen)
            if Accent.was_ambiguous(out):
                return True

        minbend = "%sm" % self._sin.backend
        bend = Backends.BACKENDS[minbend](self._sin, mincfg, minsen)
        # we keep trying until we hit the subseq
        while not bend.found:
            bend.run(self._sin.t_depth, self._sin.wgt, duration)

        return True


    def save_min_cfg(self, gp, lp):
        gd, gf = os.path.split(self._sin.gp)
        gname, gext = os.path.splitext(gf)
        _gf = "%s.%s%s" % (gname, self._sin.minp, gext)
        _gp = os.path.join(gd, _gf)
        ld, lf = os.path.split(self._sin.lp)
        lname, lext = os.path.splitext(lf)
        _lf = "%s.%s%s" % (lname, self._sin.minp, lext)
        _lp = os.path.join(ld, _lf)
        Utils.file_copy(gp, _gp)
        Utils.file_copy(lp, _lp)


    def write_stat(self, gp, lp, tag=''):
        """ write no of rules, alts, symbols
            Use the tag to mark the final line
        """
        s = "-,-,-" 
        if gp is not None:
            lex = Lexer.parse(open(lp, 'r').read())
            cfg = CFG.parse(lex, open(gp, 'r').read())
            rules, alts, syms = cfg.size()
            s = "%s,%s,%s" % (rules, alts, syms)

        with open(self.statslog, "a") as logp:
            logp.write("%s%s\n" % (tag, s))

