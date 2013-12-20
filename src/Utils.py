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


import sys, random
import CFG


def error(msg, c):
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
