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


import os, tempfile, shutil
import random
import Minimiser, AmbiParse
import CFG, Lexer, Accent
import MiniUtils
import AmbiDexter


class Min3a(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)
        if ambimin.duration is None:
            ambimin.usage("** Duration to run minimisation is not set **\n")

        if ambimin.ambijarp is None:
            ambimin.usage("** Need path to ambidexter jar file **\n")

        if ambimin.heap is None:
            ambimin.usage("** Heap size for ambidexter is not set **\n")

        if ambimin.ambi_duration is None:
            ambimin.usage("** Duration to run ambidexter is not set **\n")


        opts = ['-q', '-pg', '-ik', '0']
        self.ambidxt = AmbiDexter.AmbiDexter(self.ambimin.ambijarp, opts,
                                             self.lex_ws, self.ambimin.heap)


    def rule_alts_combs(self, cfgmap):
        combs = []
        for k in cfgmap.keys():
            if len(cfgmap[k]) > 1:
                for i in range(len(cfgmap[k])):
                    combs.append((k, i))

        return combs


    def run_accent(self, sen, gp, lp, td):
        """ build parser in td using gp+lp, and parse sentence sen."""

        parser = Accent.compile(gp, lp)
        out = Accent.run(parser, sen)
        ambiparse = AmbiParse.parse(self, out)
        _gp = tempfile.mktemp('.acc', dir=td)
        _lp = tempfile.mktemp('.lex', dir=td)
        MiniUtils.write_cfg_lex(ambiparse.min_cfg, _gp, lp, _lp)

        return _gp, _lp


    def minimise(self):
        td = tempfile.mkdtemp()
        amb, sen, trees = self.find_ambiguity(self.ambimin.gp, self.ambimin.lp)
        assert amb
        ambi_parse = AmbiParse.parse(self, trees)
        gp, lp = os.path.join(td, "0.acc"), os.path.join(td, "0.lex")
        MiniUtils.write_cfg_lex(ambi_parse.min_cfg, gp, self.ambimin.lp, lp)
        self.write_stat(gp)

        _gp, _lp = self.run(td, ambi_parse.min_cfg, gp, lp)
        self.save_min_cfg(_gp, _lp)
        shutil.rmtree(td, True)


    def run(self, td, cfg, gp, lp):
        currgp, currlp = gp, lp
        currcfg = cfg
        n = 1
        found = True

        while found:
            found = False
            combs = self.rule_alts_combs(currcfg)
            random.shuffle(combs)
            while combs:
                key, i = combs.pop()
                _cfg = MiniUtils.cfg_minus_alt(currcfg, key, i)
                _gf, _lf = "%s.acc" % n, "%s.lex" % n
                _gp, _lp = os.path.join(td, _gf), os.path.join(td, _lf)
                MiniUtils.write_cfg_lex(_cfg, _gp, currlp, _lp)
                n += 1

                if MiniUtils.valid_cfg(_gp, _lp):
                    __gp, __lp = MiniUtils.pruned_cfg(_cfg, _gp, _lp)
                    amb, sen, trees = self.find_ambiguity(__gp, __lp,
                                               self.ambimin.duration)
                    if amb:
                        ambi_parse = AmbiParse.parse(self, trees)
                        _min_gp = os.path.join(td, "min.%s" % _gf)
                        _min_lp = os.path.join(td, "min.%s" % _lf)
                        MiniUtils.write_cfg_lex(ambi_parse.min_cfg,
                                                _min_gp, __lp, _min_lp)
                        self.write_stat(_min_gp)
                        found = True
                        currcfg = ambi_parse.min_cfg
                        currgp = _min_gp
                        currlp = _min_lp
                        print "==> currp: %s " % currgp
                        break


        # run ambidexter on the minimised grammar
        ambisen, accsen = self.ambidxt.ambiguous(currgp, currlp,
                                        str(self.ambimin.ambi_duration))
        print "ambisen: " , ambisen
        print "accsen: " , accsen
        if accsen is not None:
            # pass the string from ambidexter to accent,
            # to minimisei the grammar even further
            _gp, _lp = self.run_accent(accsen, currgp, currlp, td)
            self.write_stat(_gp, '*')
            return _gp, _lp

        # AmbiDexter didn't find anything
        self.write_stat(None, '*')
        return currgp, currlp
