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


import os, sys, copy, tempfile
import Lexer, CFG, Backends, Accent
import AmbiParse
import MiniUtils, Utils


class Simple:

    def __init__(self, sin):
        self._sin = sin
        if self._sin.td is None:
            self._sin.td = tempfile.mkdtemp()

        if not os.path.exists(self._sin.td):
            os.mkdir(self._sin.td)

        self.mingp = os.path.join(self._sin.td, "%s.acc" % 0)
        self.minlp = os.path.join(self._sin.td, "%s.lex" % 0)
        self.write_cfg_lex(self._sin.ambi_parse, self.mingp, self.minlp)

        # write stats to the log for initial cfg and minimised cfg
        self.statslog = "%s/log" % self._sin.td
        open(self.statslog, "w").close()
        print "=> writing stats to %s" % self._sin.td
        self.write_stat(self._sin.gp, self._sin.lp)
        self.write_stat(self.mingp, self.minlp)


    def write_cfg_lex(self, ambi_parse, gp, lp):
        CFG.write(ambi_parse.min_cfg, gp)
        Lexer.write(ambi_parse.sym_toks, ambi_parse.toks, self._sin.lex_ws, lp)


    def cfg_minus_alt(self, cfg, rule_name, i):
        """ Create a new cfg without the respective alternative
            (rule.name.seqs[i])
        """
        _cfg = copy.deepcopy(cfg)
        _seqs = _cfg.get_rule(rule_name).seqs
        del _seqs[i]
        return _cfg


    def valid_cfg(self, cfg):
        if MiniUtils.cyclic(cfg):
            return False

        return True


    def prune_cfg(self, cfg, lex):
        """ Given a grammar (gp), prune the unreachable rules.
            The cfg is directly manipulated.
        """
        unreachable = MiniUtils.unreachable_rules(cfg)
        if len(unreachable) > 0:
            print "=> unreachable: ", unreachable
            _rules = []
            for rule in cfg.rules:
                if rule.name not in unreachable:
                    _rules.append(rule)

            return CFG.CFG(lex, cfg.sym_tokens, _rules)

        return cfg


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
            self.verify_ambiguity(gp, lp, ambstr)


    def verify_ambiguity(self, mingp, minlp, minsen, duration=None):
        print "==> verify grammar %s with minimiser %s \n" % \
                (mingp, self._sin.minp)
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
                print "** verified **"

        minbend = "%sm" % self._sin.backend
        if minbend in Backends.BACKENDS:
            bend = Backends.BACKENDS[minbend](self._sin, mincfg, minsen)
        else:
            bend = Backends.WGTBACKENDS[minbend](self._sin, mincfg, minsen)

        # we keep trying until we hit the subseq
        while not bend.found:
            bend.run(self._sin.t_depth, self._sin.wgt, duration)

        print "** verified **"


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

