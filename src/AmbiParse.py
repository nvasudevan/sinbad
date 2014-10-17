#! /usr/bin/env python

import sys, re
from sets import Set
import Utils


class AmbiParse:

    def __init__(self, out):
        self.parseout = out
        self.parse_tree = []


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
                
        ambstr = " ".join(x for x in minamb)
        #print "ambstr: " , ambstr
        return minamb


    def parse_vamb(self):
        tree1 = Utils.lines_between_patterns(self.parseout, "TREE 1", "TREE 2")
        tree2 = Utils.lines_between_patterns(self.parseout, "TREE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)


    def parse_hamb(self):
        tree1 = Utils.lines_between_patterns(self.parseout, "PARSE 1", "PARSE 2")
        tree2 = Utils.lines_between_patterns(self.parseout, "PARSE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)


    def parse_rhs(self, l):
        i = 0
        rhs = []
        while i < len(l):
            if l[i] == "{":
                j = Utils.match_bkt(l, i+1)
                i = j
                continue
            else:
                rhs.append(l[i])
                
            i += 1
            
        return rhs


    def rule(self, amb, i):
        rule_name = amb[i-1]
        # find the corresponding '}'
        j = Utils.match_bkt(amb, i+1)
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


    def min_cfg(self, amb1, amb2):
        cfg = {}
        for amb in amb1,amb2:
            # parse root rule 
            lhs,rhs,i = self.root_rule(amb)
            if lhs not in cfg.keys():
                cfg[lhs] = [] 
    
            cfg[lhs].append(rhs)
            j = i
            while j < len(amb):
                if amb[j] == "{":
                    # j -1 is a rule
                    lhs,rhs = self.rule(amb, j)
                    if lhs not in cfg.keys():
                        cfg[lhs] = []

                    cfg[lhs].append(rhs)
                j += 1
            
        return cfg


def parse(out):
    ambiparse = AmbiParse(out)
    vamb_pat = "Two different ``[a-zA-Z0-9_-]*'' derivation trees for the same phrase."
    vamb = False
    for l in iter(ambiparse.parseout.splitlines()):
        if re.match(vamb_pat, l):
            vamb = True
            break

    amb1,amb2 = None, None
    if vamb:
        print "\ntype: vertical"
        amb1,amb2 = ambiparse.parse_vamb()
    else:
        print "\ntype: horizontal"
        amb1,amb2 = ambiparse.parse_hamb()

    return ambiparse.min_cfg(amb1,amb2)


if __name__ == "__main__":
    parse(open(sys.argv[1], 'r').read())

