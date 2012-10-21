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

class MutateGrammar:

	def __init__(self, gf, lf, cnt):
		self.lex = Lexer.parse(open(lf, "r").read())
		self.cfg = CFG.parse(self.lex, open(gf, "r").read())
		self.symbolic_tokens = []
		gf_lines = open(gf, "r").readlines()
		header = "%nodefault\n\n"
		for line in gf_lines:
		    if line.startswith("%token"):
		        self.symbolic_tokens = line[6:line.index(";")].replace(" ","").split(",")
		        header = "{0}\n%nodefault\n\n".format(line)
		        break
		
		g_dir, g_file = os.path.dirname(gf), os.path.basename(gf)
		self.variations_cnt = cnt
		i = 1
		while i <= self.variations_cnt:
			_cfg = self.modify_grammar()
			_f_file = open(('%s/%s_%s.spec' % (g_dir, os.path.splitext(g_file)[0], i)),"w")
			_f_file.write(header)
			_f_file.write(self.cfg_repr(_cfg))
			_f_file.close()
			i += 1
			

	def cfg_repr(self, cfg):
		_cfg_repr = ""
		for rule in cfg.rules:
		    rule_seqs = []
		    for seq in rule.seqs:
		        _seq = []
		        for tok in seq:
		            if isinstance(tok, CFG.Term):
		                _tok = tok
		                _tok = str(_tok).replace("'","")
		                if self.symbolic_tokens.__contains__(_tok):
		                    _seq.append(_tok)
		                    continue

		            _seq.append(tok)
		        
		        rule_seqs.append(" ".join([str(x) for x in _seq]))

		    _cfg_repr += (('%s : %s' % (rule.name, " | ".join(rule_seqs))) + "\n;\n")
		return _cfg_repr


	def modify_seq(self, rule):
		i_seq = random.randint(0, rule.seqs.__len__()-1)
		seq =  rule.seqs[i_seq]
		tokens = [rule.name for rule in self.cfg.rules if rule.name != 'root']
		tokens += self.lex.keys()
		random.shuffle(tokens)
		_tok = random.choice(tokens)
		if self.lex.keys().__contains__(_tok):
			tok = CFG.Term(_tok)
		else:
			tok = CFG.Non_Term_Ref(_tok)
            
		if seq.__len__() == 0: 
			seq.append(tok)
		else:
			i = random.randint(0, seq.__len__() - 1) # pick a random token
			seq[i] = tok
                 
    
	def modify_grammar(self):
		cloned_g = self.cfg.clone()
		rule_keys = [rule.name for rule in cloned_g.rules]
		key_to_modify = random.choice(rule_keys)
		print key_to_modify
		rule = cloned_g.get_rule(key_to_modify)
		print "++ rule: ", rule
		_which = random.choice([0,1])
		if (_which == 0) and (not rule.seqs.__contains__([])):
			rule.seqs.append([])
		else: 	
			self.modify_seq(rule)
			
		print "-- rule: ", rule
	    
		return cloned_g


def generate(cfg, lex, cnt):
	MutateGrammar(cfg, lex, cnt)
	
	
if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1 : ], "hn:")
	cnt = None
	if len(args) == 0:
	    sys.stderr.write("MutateGrammar.py -n <number of variations to generate> <grammar> <lexer> \n")
	    sys.exit(1)
	if len(args) % 2 != 0:
	    sys.stderr.write("MutateGrammar.py -n <number of variations to generate> <grammar> <lexer> \n")
	    sys.exit(1)
	for opt in opts:
		if opt[0] == "-n":
			cnt = int(opt[1])
		
	if cnt == None:
		sys.stderr.write("Provide -n <no of variations> \n\n")
		sys.exit(1)
        
	generate(args[0], args[1], cnt)
