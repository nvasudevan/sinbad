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


import sys, re, tempfile
from sets import Set
import CFG, Lexer


VERTICAL_AMBIGUITY = "Two different ``[a-zA-Z0-9_-]*'' derivation trees for the same phrase."
TERM_TOK = "'(.)'"


class AmbiParse:

    def __init__(self, lp, lex_ws, ptrees):
        self.lex = Lexer.parse(open(lp, 'r').read())
        self.lex_ws = lex_ws
        self.ptrees = ptrees
        self.amb_type = 'horizontal'
        for l in iter(self.ptrees.splitlines()):
            if re.match(VERTICAL_AMBIGUITY, l):
                self.amb_type = 'vertical'
                break

        amb1, amb2 = None, None
        if self.amb_type == 'vertical':
            amb1, amb2 = self.parse_vamb()
        else:
            amb1, amb2 = self.parse_hamb()

        # extract the ambiguous string from sentence
        amb1s = self.ambiguous_string(amb1)
        amb2s = self.ambiguous_string(amb2)
        assert amb1s == amb2s
        self.amb_str = amb1s

        # extract the ambiguous grammar rules from parse trees
        _cfg = self.ambiguous_cfg_subset(amb1, amb2)
        # first, minimise the lex based on the cfg
        self.sym_toks, self.toks = self.minimise_lex(_cfg)
        tp = tempfile.mktemp()
        Lexer.write(self.sym_toks, self.toks, self.lex_ws, tp)
        lex = Lexer.parse(open(tp, 'r').read())

        # convert _cfg to a CFG instance.
        self.min_cfg = self.to_CFG(_cfg, lex)


    def minimise_lex(self, cfg):
        """ Iterate through the cfg's rules and build the lex tokens. """
        _sym_tokens = Set()
        _tokens = Set()
        for key in cfg.keys():
            seqs = cfg[key]
            for seq in seqs:
                for e in seq:
                    if e.startswith("'"):
                        _tokens.add(e.replace("'", ""))
                    else:
                        if e in self.lex.keys():
                            _sym_tokens.add(e)

        sym_toks, toks = {}, {}
        for e in _sym_tokens:
            sym_toks[e] = self.lex[e]

        for e in _tokens:
            toks[e] = e

        return sym_toks, toks


    def to_CFG(self, cfg, lex):
        """ At present, I have taken an easier approach to create CFG.
            I write the token line and the rules to a temp file and
            read that back. An alternative way (without I/O) would be
            to iterate through the rules and build your CFG instance.
        """
        tp = tempfile.mktemp()
        header = ""
        if len(self.sym_toks) > 0:
            header = "%token " + "%s;" % (", ".join(t for t in self.sym_toks))

        with open(tp, 'w') as tf:
            tf.write(('%s\n\n' % header) + "%nodefault\n\n")
            pp_seqs = Set()
            for seq in cfg['root']:
                seq_s = " ".join(str(e) for e in seq)
                pp_seqs.add(seq_s)

            tf.write("%s : %s\n;\n" % ('root', " | ".join(pp_seqs)))

            nt_list = [nt for nt in cfg.keys() if nt != 'root']
            nt_list.sort()
            for k in nt_list:
                pp_seqs = []
                seqs = cfg[k]
                for seq in seqs:
                    seq_s = " ".join(str(e) for e in seq)
                    pp_seqs.append(seq_s)

                tf.write("%s : %s\n;\n" % (k, " | ".join(pp_seqs)))

        return CFG.parse(lex, open(tp, 'r').read())


    def ambiguous_string(self, ambtokl):
        """ returns the 'actual' ambiguous string from the parse tree """
        _terms = []
        for tok in ambtokl:
            if tok not in ['{', '}']:
                if (tok in self.lex):
                    _terms.append(self.lex[tok])
                elif (re.match(TERM_TOK, tok)):
                    ## CHECK!! ##
                    _terms.append(tok.replace("'", ""))

        if self.lex_ws:
            # CSS has WS for a single space, so we build sentence
            # without whitespaces
            return "".join(t for t in _terms)

        return " ".join(t for t in _terms)


    def min_amb_tokens(self, lines):
        minamb = []
        for l in lines:
            if "alternative" in l:
                # non-term
                ltokens = l.split()
                # K alternative .... { -  we need first and last token only
                minamb.append(ltokens[0])
                minamb.append(ltokens[-1])
            else:
                ltokens = l.split()
                # contains terminal (only one token)
                minamb.append(ltokens[0])

        return minamb


    def parse_output(self, out, startp, endp):
        match = False
        lines = []
        for l in iter(out.splitlines()):
            if re.match(startp, l):
                match = True
                continue
            elif re.match(endp, l):
                match = False
                continue
            elif match:
                if l != "":
                    lines.append(l)

        return lines


    def match_bkt(self, l, i):
        bkcnt = 1
        k = i
        while k < len(l):
            if l[k] == '{':
                bkcnt += 1
            elif l[k] == '}':
                bkcnt -= 1

            if bkcnt == 0:
                return k + 1

            k += 1

        return None


    def parse_vamb(self):
        tree1 = self.parse_output(self.ptrees, "TREE 1", "TREE 2")
        tree2 = self.parse_output(self.ptrees, "TREE 2", "------")

        return self.min_amb_tokens(tree1), self.min_amb_tokens(tree2)


    def parse_hamb(self):
        tree1 = self.parse_output(self.ptrees, "PARSE 1", "PARSE 2")
        tree2 = self.parse_output(self.ptrees, "PARSE 2", "------")

        return self.min_amb_tokens(tree1), self.min_amb_tokens(tree2)


    def parse_rhs(self, l):
        i = 0
        rhs = []
        while i < len(l):
            if l[i] == "{":
                j = self.match_bkt(l, i+1)
                i = j
                continue
            else:
                rhs.append(l[i])

            i += 1

        return rhs


    def rule(self, amb, i):
        rule_name = amb[i-1]
        # find the corresponding '}'
        j = self.match_bkt(amb, i+1)
        assert j is not None
        rhs = self.parse_rhs(amb[i+1:j-1])

        return rule_name, rhs


    def root_rule(self, amb):
        root_amb = list(amb)
        if root_amb[0] == 'root':
            # parse already contain root rule
            lhs, rhs = self.rule(root_amb, 1)
            return lhs, rhs, 2

        root_amb.insert(0, '{')
        root_amb.insert(0, 'root')
        root_amb.append('}')
        lhs, rhs = self.rule(root_amb, 1)
        return lhs, rhs, 0


    def ambiguous_cfg_subset(self, amb1, amb2):
        """ From amb1 and amb2, extract the (minimised) CFG """
        cfg = {}
        for amb in amb1, amb2:
            # parse root rule
            lhs, rhs, i = self.root_rule(amb)
            if lhs not in cfg.keys():
                cfg[lhs] = []

            if rhs not in cfg[lhs]:
                cfg[lhs].append(rhs)

            j = i
            while j < len(amb):
                if amb[j] == "{":
                    # j -1 is a rule
                    lhs, rhs = self.rule(amb, j)
                    if lhs not in cfg.keys():
                        cfg[lhs] = []

                    if rhs not in cfg[lhs]:
                        cfg[lhs].append(rhs)

                j += 1

        return cfg


def parse(lex, lex_ws, out):
    ambiparse = AmbiParse(lex, lex_ws, out)

    return ambiparse
