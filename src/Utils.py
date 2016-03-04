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


import os, subprocess, sys, random, re, time
import CFG, Lexer


def error(msg, c=1):
    sys.stderr.write(msg)
    sys.exit(c)


def min_max(l):
    assert len(l) > 0
    min = max = l[0]
    minc = maxc = 1
    for e in l[1:]:
        if e == min:
            minc += 1
        elif e < min:
            min = e
            minc = 1

        if e == max:
            maxc += 1
        elif e > max:
            max = e
            maxc = 1

    return min, minc, max, maxc


# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
def rws(scores):
    """select a score based on roulette wheel selection"""
    rndscore = random.random() * sum(scores)

    for i, sc in enumerate(scores):
        rndscore -= sc
        if rndscore < 0:
            return i


def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)


def rankdata(a):
    n = len(a)
    ivec=rank_simple(a)
    svec=[a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0]*n
    for i in xrange(n):
        sumranks += i
        dupcount += 1
        if i==n-1 or svec[i] != svec[i+1]:
            averank = sumranks / float(dupcount) + 1
            for j in xrange(i-dupcount+1,i+1):
                newarray[ivec[j]] = averank
            sumranks = 0
            dupcount = 0
    return newarray


def rbrws(scores):
    """ Rank based roulette wheel selection 
        e.g: scores of [0.1,0.3,0.2] will result in a rank of [1,3,2]"""
    ranks = rankdata(scores)
    i = rws(ranks)
    return i


def find_terminating_indices(cfg_rules):
    """ Returns a map containing rule to index, where index refers to one of
        the sequence of the rule, which when selected guarantees termination"""
    terminating_indices = {}
    found = True
    while (found):
        found = False
        for rule in cfg_rules:
            rule_seqs = []
            for i,seq in enumerate(rule.seqs):
                _seq = []
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
                        if e.name not in terminating_indices.keys():
                            _seq.append(e.name)

                if len(_seq) == 0:
                    if not terminating_indices. __contains__(rule.name):
                        found = True
                        terminating_indices[rule.name] = i

    return terminating_indices


def find_terminating_indices2(cfg_rules):
    """ Essentially same ideas as above but with small variation: for each rule,
        we have multiple indices referring to sequences for guaranteed termination"""
    terminating_indices = {}
    found = True
    while (found):
        found = False
        for rule in cfg_rules:
            indices = []
            for i,seq in enumerate(rule.seqs):
                _seq = []
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
                        if e.name not in terminating_indices.keys():
                            _seq.append(e.name)

                if len(_seq) == 0:
                    if not terminating_indices. __contains__(rule.name):
                        indices.append(i)

            if len(indices) > 0:
                found = True
                terminating_indices[rule.name] = indices

    return terminating_indices


def calc_seqs_finite_depth(cfg):
    for rule in cfg.rules:
        rule.seqs_finite_depth = []

    while 1:
        changed = False
        for rule in cfg.rules:
            if len(rule.seqs_finite_depth) > 0:
                continue

            for i,seq in enumerate(rule.seqs):
                _seq = []
                for e in seq:
                    if isinstance(e, CFG.Non_Term_Ref):
                        ref_rule = cfg.get_rule(e.name)
                        if len(ref_rule.seqs_finite_depth) == 0:
                            _seq.append(e.name)
                            break

                if len(_seq) == 0:
                    changed = True
                    rule.seqs_finite_depth.append(i)
                    break


        if not changed:
            break


def file_copy(source, target):
    r = subprocess.call(["cp", source, target])
    if r != 0:
        Utils.error("Copy of %s -> %s failed!\n" % (source, target), r)

    print "Copied: %s -> %s\n" % (source, target)



def time_elapsed(start, duration):
   now = time.time()
   #print "now: %s, start: %s, duration: %s, diff: %s" % (now, start, duration, (now - start))
   if (now - start) > duration: 
       return True
   
   return False

