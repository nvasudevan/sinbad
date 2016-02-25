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

from sets import Set
import os, copy
import CFG


def remove_terminals(cfg):
    rules, indices, rules_to_remove = {}, {}, []
    for rule in cfg.rules:
        rule_seqs = []
        for i, seq in enumerate(rule.seqs):
            _seq = []
            for e in seq:
                if isinstance(e, CFG.Non_Term_Ref):
                    _seq.append(e.name)

            if len(_seq) == 0:
                if rule.name not in indices.keys():
                    indices[rule.name] = i
                    rules_to_remove.append(rule.name)

            rule_seqs.append(_seq)

        if rule.name not in indices.keys():
            rules[rule.name] = rule_seqs
            
    return rules, indices, rules_to_remove


def remove_matched_rule_refs(rules, indices):
    _r_remove = []
    for key in rules.keys():
        rule_seqs = []
        for ind, seq in enumerate(rules[key]):
            _seq = []
            for e in seq:
                if e not in indices.keys():
                    _seq.append(e)
            if len(_seq)== 0:
                indices[key] = ind
                _r_remove.append(key)
                break

            rule_seqs.append(_seq)
                
        rules[key] = rule_seqs
        
    return _r_remove

       
def cyclic(cfg):
    rules, indices, removed = remove_terminals(cfg)
    
    if len(removed) > 0:
        while True:
            removed = remove_matched_rule_refs(rules, indices)
            if len(removed) == 0:
                break
                
            for k in removed:
                del rules[k]
        
    cyclic_rules = []
    for key in rules.keys():
        if key not in indices.keys():
            cyclic_rules.append("%s : %s" % (key, rules[key]))

    if len(cyclic_rules) > 0:
        return True

    return False


def valid_cfg(gp, lex):
    cfg = CFG.parse(lex, open(gp, "r").read())
    if cyclic(cfg):
        return False

    return True


def cfg_minus_alt(cfg, rule_name, i):
    """ Create a new cfg without the respective alternative
        (rule.name.seqs[i])"""
        
    _cfg = {}
    for rule in cfg.rules:
        rhs = []
        seqs = rule.seqs
        for j in range(len(seqs)):
            if not (rule.name == rule_name and j == i):
                rhs.append(seqs[j]) 
             
        _cfg[rule.name] = rhs

    return _cfg


def unreachable_rules(cfg):
    """ Checks if every non-terminal is reachable from start symbol
        we build this reachable non-terms in two phases: 
        1) build the initial list from root rule; 
        2) now iterate through the list, and add reachable non-terms"""

    root_rule = cfg.rules[0]
    nonterms = [(rule.name) for rule in cfg.rules \
                       if rule.name != root_rule.name]

    reach_nonterms = Set()
    for seq in root_rule.seqs:
        for e in seq:
            if isinstance(e, CFG.Non_Term_Ref):
                reach_nonterms.add(e.name)

    # we use the initial set to start of searching for reachability
    exploring = copy.copy(reach_nonterms)
    # keep track of symbols for which we have explored reachability
    explored = Set()
    while len(exploring) > 0:
        name = exploring.pop()
        explored.add(name)
        rule = cfg.get_rule(name)
        for seq in rule.seqs:
            for e in seq:
                if isinstance(e, CFG.Non_Term_Ref):
                    reach_nonterms.add(e.name)
                    if e.name not in explored:
                        exploring.add(e.name)

    return set(nonterms) - set(reach_nonterms)
