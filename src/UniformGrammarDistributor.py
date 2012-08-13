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


import getopt, sys, os, random, math
import CFG, Lexer

class UniformGrammarDistributor:

	def __init__(self, gf, lf, cnt):
		self.lex = Lexer.parse(open(lf, "r").read())
		self.cfg = CFG.parse(self.lex, open(gf, "r").read())
		g_dir, g_file = os.path.dirname(gf), os.path.basename(gf)
		self.variations_cnt = cnt
		i = 1
		while i <= self.variations_cnt:
			_cfg = self.modify_grammar()
			_f_file = open(('%s/%s_%s.spec' % (g_dir, os.path.splitext(g_file)[0], i)),"w")
			_f_file.write("%nodefault\n\n")
			_f_file.write(self.cfg_repr(_cfg))
			_f_file.close()
			i += 1


	def cfg_repr(self, cfg):
		_cfg_repr = ""
		for rule in cfg.rules:
		    rule_seqs = []
		    for seq in rule.seqs:
		        rule_seqs.append(" ".join([str(x) for x in seq]))
		    _cfg_repr += (('%s : %s' % (rule.name, " | ".join(rule_seqs))) + "\n;\n")
		return _cfg_repr
            
	# we either change a token or add a empty alternative
	#def modify_seq(self, seq):
	def modify_rule(self, rule):
		print "++ " , rule		
		_which = random.choice([0,1]) # 0 - empty, 1 - modify token
		if _which == 0:
			last_seq = rule.seqs[rule.seqs.__len__()-1]
			print last_seq
			if last_seq.__len__() != 0: # add emplty sequence if the last seq is not empty
				rule.seqs.append([])
				print "empty: " , rule.seqs
		else:
			i_seq = random.randint(0, rule.seqs.__len__() - 1) # pick a random sequence
			seq = rule.seqs[i_seq]
			print "++ " , seq
			tokens = [rule.name for rule in self.cfg.rules if rule.name != 'root']
			tokens += self.lex.keys()
			random.shuffle(tokens)
			_tok = random.choice(tokens)
			print "_tok: " , _tok
			print self.lex.keys()
			if self.lex.keys().__contains__(_tok):
				print "term"
				tok = CFG.Term(_tok)
			else:
				print "nonterm"
				tok = CFG.Non_Term_Ref(_tok)
	
			if seq.__len__() == 0:  # for empty sequence
				seq.append(tok)
			else:
				i = random.randint(0, seq.__len__() - 1) # pick a random token
				seq[i] = tok
			print "-- " , seq
        

	# Given a grammar, we generate grammar with one variation:
	# - pick a random sequence and then replace a random token with another (term or nonterm)
	def modify_grammar(self):
		cloned_g = self.cfg.clone()
		rule_keys = [rule.name for rule in cloned_g.rules]
		f_modify = 0.1 # modify 10% of the rules
		modify_count = random.randint(1, int(math.ceil(rule_keys.__len__() * f_modify)))
		modify_keys = random.sample(rule_keys, modify_count)
	
		for key in modify_keys:
			rule = cloned_g.get_rule(key)
			print "------ %s -------" % key
			self.modify_rule(rule)
			print "\n"

		return cloned_g

def generate(cfg, lex, cnt):
	UniformGrammarDistributor(cfg, lex, cnt)

if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1 : ], "hn:")
	cnt = None
	if len(args) == 0:
	    sys.stderr.write("uniform_grammar_distribution.py -n <number of variations to generate> <grammar> <lexer> \n")
	    sys.exit(1)
	if len(args) % 2 != 0:
	    sys.stderr.write("uniform_grammar_distribution.py -n <number of variations to generate> <grammar> <lexer> \n")
	    sys.exit(1)
	for opt in opts:
		if opt[0] == "-n":
			cnt = int(opt[1])
		
	if cnt == None:
		sys.stderr.write("Provide -n <no of variations> \n\n")
		sys.exit(1)
        
	generate(args[0], args[1], cnt)
