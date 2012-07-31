#! /usr/bin/env python

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

# This program generates random grammars in ACCENT format. To see usage, run it with -h. 

import getopt, sys, os, string, random, math

class RandomGrammarGenerator:

    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1 : ], "hn:d:")
        if len(opts) == 0:
            self.usage("Not enough arguments.")
            
        self.grammar_dir, self.N_grammars = None, None
        for opt in opts:
            if opt[0] == "-d":
                self.grammar_dir = opt[1]
            elif opt[0] == "-n":
                self.N_grammars = int(opt[1])
            elif opt[0] == "-h":
                self.usage()                
            else:
                self.usage("Unknown argument '%s'" % opt[0])
                
        # few initialisation constants
        self.max_no_alternatives = 5
        self.max_tokens_per_rule = 7
        self.min_ratio_empty_lhs = 0.1
        self.max_ratio_empty_lhs = 0.2
        
        if not os.path.exists(self.grammar_dir):
            os.makedirs(self.grammar_dir)

        i = 1
        while i <= self.N_grammars:
            self.generate_grammar(str(i))
            i += 1

        
    def usage(self, msg = None):
            if msg is not None:
                    sys.stderr.write(msg + "\n\n")

            sys.stderr.write("generate_grammars_python -d <grammar directory> -n <no of grammars to generate>\n")
            sys.exit(1)


    def generate_grammar(self, grammar):
        if not os.path.exists(self.grammar_dir + "/" + grammar):
            os.makedirs(self.grammar_dir + "/" + grammar)

        rules = {}
        # to control no of empty alternatives,
        min_empty = math.ceil(len(string.uppercase) * self.min_ratio_empty_lhs)
        max_empty = math.ceil(len(string.uppercase) * self.max_ratio_empty_lhs)
        empty_lhs_count = random.randint(min_empty, max_empty)
        epsilon_rules = random.sample(string.uppercase, empty_lhs_count)
        grammar_file =  open(self.grammar_dir + "/" + grammar + "/" + grammar + ".spec","w")
        rules['root'] = self.generate_rule('root')
        grammar_file.write("%nodefault\n\nroot : " + self.rule_repr(rules['root']) + "\n;\n")
        
        for lhs in string.uppercase:
            rules[lhs] = self.generate_rule(lhs)
            if epsilon_rules.__contains__(lhs):
                rules[lhs].append("")
            grammar_file.write(lhs + " : " + self.rule_repr(rules[lhs]) + "\n;\n")
            
        grammar_file.close()


    def generate_rule(self, rule):
        alternatives = []
        max_alternatives_lhs = random.randint(1, self.max_no_alternatives)
        while (len(alternatives) < max_alternatives_lhs):
            alternative = []
            tokens_per_rule = random.randint(1, self.max_tokens_per_rule)
            while (len(alternative) < tokens_per_rule):
                token = random.choice(string.letters)
                if string.find(string.lowercase,token) != -1:
                    alternative.append("'" + token + "'")
                else:
                    alternative.append(token)
            alternatives.append(alternative)
            
        return alternatives   


    def rule_repr(self, alts):
        alts_string = []
        for alt in alts:
            alts_string.append(" ".join([str(token) for token in alt]))
        return " | ".join([x for x in alts_string])


RandomGrammarGenerator()
