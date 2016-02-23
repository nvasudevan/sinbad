#! /usr/bin/env python

import sys, re
from sets import Set
import Utils

VERTICAL_AMBIGUITY = "Two different ``[a-zA-Z0-9_-]*'' derivation trees for the same phrase."
TERM_TOK = "'(.)'"

class AmbiParse:

    def __init__(self, min, out):
        self.min = min
        self.parse_out = out
        self.vamb = False
        for l in iter(out.splitlines()):
            if re.match(VERTICAL_AMBIGUITY, l):
                self.vamb = True
                break
    
        self.amb1, self.amb2 = None, None
        if self.vamb:
            #print "\ntype: vertical"
            self.amb1, self.amb2 = self.parse_vamb()
        else:
            #print "\ntype: horizontal"
            self.amb1, self.amb2 = self.parse_hamb()
    


    def ambiguous_subset(self):
        """ returns the 'actual' ambiguous string from the parse tree """
        _terms = []
        for tok in self.amb1:
            if (tok in self.min.lex) or (re.match(TERM_TOK, tok)):
                _terms.append(tok)

        amb_str = " ".join(t for t in _terms)

        return  amb_str.replace("'","")


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


    def lines_between_patterns(self, out, startp, endp):
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
        tree1 = self.lines_between_patterns(self.parse_out, "TREE 1", "TREE 2")
        tree2 = self.lines_between_patterns(self.parse_out, "TREE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)


    def parse_hamb(self):
        tree1 = self.lines_between_patterns(self.parse_out, "PARSE 1", "PARSE 2")
        tree2 = self.lines_between_patterns(self.parse_out, "PARSE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)


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

        return rule_name,rhs  


    def root_rule(self, amb):
        root_amb = list(amb)
        if root_amb[0] == 'root':
            # parse already contain root rule
            lhs,rhs = self.rule(root_amb, 1)
            return lhs,rhs,2

        root_amb.insert(0,'{')
        root_amb.insert(0,'root')
        root_amb.append('}')
        lhs,rhs = self.rule(root_amb, 1)
        return lhs,rhs,0


    def ambiguous_cfg_subset(self):
        """ From amb1 and amb2, extract the (minimised) CFG """
        cfg = {}
        for amb in self.amb1, self.amb2:
            # parse root rule 
            lhs,rhs,i = self.root_rule(amb)
            if lhs not in cfg.keys():
                cfg[lhs] = [] 
    
            if rhs not in cfg[lhs]:
                cfg[lhs].append(rhs)

            j = i
            while j < len(amb):
                if amb[j] == "{":
                    # j -1 is a rule
                    lhs,rhs = self.rule(amb, j)
                    if lhs not in cfg.keys():
                        cfg[lhs] = []

                    if rhs not in cfg[lhs]:
                        cfg[lhs].append(rhs)

                j += 1
            
        return cfg


def parse(min, out):
    ambiparse = AmbiParse(min, out)

    return ambiparse


