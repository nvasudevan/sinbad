#! /usr/bin/env python

import sys, re
from sets import Set


class AmbiParse:

    def __init__(self, out):
        self.parseout = out
        self.parse_tree = []


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
        tree1 = self.lines_between_patterns(self.parseout, "TREE 1", "TREE 2")
        tree2 = self.lines_between_patterns(self.parseout, "TREE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)
            
            
    def parse_hamb(self):
        tree1 = self.lines_between_patterns(self.parseout, "PARSE 1", "PARSE 2")
        tree2 = self.lines_between_patterns(self.parseout, "PARSE 2", "------")

        return self.min_amb_tokens(tree1),self.min_amb_tokens(tree2)


    def match_bkt(self, s, i):
        bkcnt = 1
        k = i + 1
        while k < len(s):
            if s[k] == '{':
                bkcnt += 1
            elif s[k] == '}':
                bkcnt -= 1
                
            if bkcnt == 0:
                return k + 1
                
            k += 1
            
        return None            


    def parse_rhs(self, s):
        i = 0
        rhs = []
        while i < len(s):
            if s[i] == "{":
                j = self.match_bkt(s, i)
                i = j
                continue
            else:
                rhs.append(s[i])
                
            i += 1
            
        return rhs


    def rule(self, amb, i):
        rule_name = amb[i-1]
        # find the corresponding '}'
        j = self.match_bkt(amb, i)
        assert j is not None
        _rhs = amb[i+1:j-1]
        rhs = self.parse_rhs(_rhs)
        rhs_str = " ".join(x for x in rhs)
        return rule_name,rhs_str  


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
                cfg[lhs] = Set() 
    
            cfg[lhs].add(rhs)
            j = i
            while j < len(amb):
                if amb[j] == "{":
                    # j -1 is a rule
                    lhs,rhs = self.rule(amb, j)
                    if lhs not in cfg.keys():
                        cfg[lhs] = Set()

                    cfg[lhs].add(rhs)
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

