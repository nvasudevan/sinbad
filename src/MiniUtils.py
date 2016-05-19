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
import os, sys, copy
import tempfile
import CFG, Lexer
import Utils

def remove_terminals(cfg):
    """ does two things:
        1) rules - set of rules without any terminals
        2) indices, rules_to_remove - initial set of rule+alt
           combination that are 0 length and can be removed
    """
    rules, indices = {}, {}
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

            rule_seqs.append(_seq)

        if rule.name not in indices.keys():
            rules[rule.name] = rule_seqs

    return rules, indices


def remove_matched_rule_refs(rules, indices):
    _r_remove = []
    for key in rules.keys():
        rule_seqs = []
        for ind, seq in enumerate(rules[key]):
            _seq = []
            for e in seq:
                if e not in indices.keys():
                    _seq.append(e)

            if len(_seq) == 0:
                indices[key] = ind
                _r_remove.append(key)
                break

            rule_seqs.append(_seq)

        rules[key] = rule_seqs

    return _r_remove


def cyclic(cfg):
    rules, indices = remove_terminals(cfg)

    rules_terminated = indices.keys()
    if len(rules_terminated) > 0:
        while True:
            rules_terminated = remove_matched_rule_refs(rules, indices)
            if len(rules_terminated) == 0:
                break

            for k in rules_terminated:
                del rules[k]

    cyclic_rules = []
    for key in rules.keys():
        if key not in indices.keys():
            cyclic_rules.append("%s : %s" % (key, rules[key]))

    if len(cyclic_rules) > 0:
        return True

    return False


def purge_dangling_refs(cfg, rule):
    """ keep purging dangling refs until there are no more
        dangling refs. Start with 'rule'
    """
    found = True
    _rules = [rule]
    currcfg = cfg

    print "cfg: ", currcfg

    while found:
        found = False
        _cfg = {}
        for k in cfg.keys():
            _seqs = []
            for seq in cfg[k]:
                if len(seq) > 0:
                    _seq = [e for e in seq if e not in _rules]
                else:
                    # pass empty alts as is
                    _seq = []

                # only add if the modify alt has len > 0
                # that is, don't add an empty alt
                if len(_seq) > 0:
                    _seqs.append(_seq)

            if len(_seqs) > 0:
                _cfg[k] = _seqs
            else:
                # a rule with no alts - remove!
                found = True
                _rules.append(k)

        currcfg = _cfg

    print "**cfg: ", currcfg


def unreachable_rules(cfg):
    """ Checks if every non-terminal is reachable from start symbol
        we build this reachable non-terms in two phases:
        1) build the initial list from root rule;
        2) now iterate through the list, and add reachable non-term
    """
    root = cfg.rules[0]
    nonterms = [(rule.name) for rule in cfg.rules if rule.name != root.name]
    reach_nonterms = Set()
    for seq in root.seqs:
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
