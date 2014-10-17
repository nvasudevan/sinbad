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


import copy, re



_RE_ID = re.compile("[a-zA-Z_][a-zA-Z_0-9]*")
_RE_OPTIONS = re.compile(".nodefault")
_RE_TOKEN = re.compile("""'(.*?)'|"(.*?)\"""")



class CFG:
    def __init__(self, tokens, rules):
        self.tokens = tokens
        self.rules = rules
        self.start_rulen = self.rules[0].name
        self._rules_dict = {}
        for r in rules:
            self._rules_dict[r.name] = r


    def clone(self):
        """ Returns a complete clone of this CFG. The clone and anything it
            points to can be changed in arbitrary ways without affecting
            the original. """
        return copy.deepcopy(self)


    def get_rule(self, name):
        return self._rules_dict[name]


    def gen_token(self, name):
        if name in self.tokens:
            return self.tokens[name]
        else:
            return name.lower()


    def __repr__(self):
        return "\n".join([str(x) for x in self.rules])



class Rule:
    def __init__(self, name, seqs):
        self.name = name
        self.seqs = seqs


    def __repr__(self):
        pp_seqs = []
        for seq in self.seqs:
            pp_seqs.append(" ".join([str(x) for x in seq]))
        return "%s : %s;" % (self.name, " | ".join(pp_seqs))



class Non_Term_Ref:
    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return self.name



class Term:
    def __init__(self, tok):
        self.tok = tok


    def __repr__(self):
        return "'%s'" % self.tok



class Sym_Term:
    def __init__(self, tok):
        self.tok = tok


    def __repr__(self):
        return "%s" % self.tok



class _Parser:
    def parse(self, lex, cfg):
        self._cfg = cfg
        rules = []
        self._toks = lex
        self._sym_toks = []
        i = 0
        while i < len(self._cfg):
            i = self._ws(i)

            j, r = self._rule(i)
            if j > i:
                rules.append(r)
                i = j
                continue

            j = self._tokens(i)
            if j > i:
                i = j
                continue

            j, _ = self._option(i)
            if j > i:
                i = j
                continue

        return CFG(self._toks, rules)


    def _ws(self, i):
        while i < len(self._cfg) and self._cfg[i] in " \n\r\t":
            i += 1
        return i


    def _id(self, i):
        m = _RE_ID.match(self._cfg, i)
        if not m:
            return i, None
        return m.end(0), m.group()


    def _tokens(self, i):
        if not self._cfg.startswith("%token", i):
            return i
        i += 6
        while self._cfg[i] != ";":
            i += 1

        _sym_tok_s = self._cfg[7:i]
        self._sym_toks = _sym_tok_s.replace(' ','').split(',')
        return i + 1


    def _rule(self, i):
        j, name = self._id(i)
        if j == i:
            return i, None
        i = self._ws(j)
        assert self._cfg[i] == ":"

        seqs = []
        while True:
            j = self._empty_seq(i)
            if j > i:
                seqs.append([])
                i = j
                if self._cfg[i] == ";":
                    i += 1
                    return i, Rule(name, seqs)
            else: 
                i += 1
                break
                            	
        while i < len(self._cfg):
            i = self._ws(i)
            j, seq = self._seq(i)
            if j > i:
                seqs.append(seq)
                i = j
                continue

            if self._cfg[i] == ";":
                return i + 1, Rule(name, seqs)

            assert self._cfg[i] == "|"

            while True:
                j = self._empty_seq(i)
                if j > i:
                    seqs.append([])
                    i = j
                    if self._cfg[i] == ";":
                        i += 1
                        return i, Rule(name, seqs)
                else: 
                    i += 1
                    break
            
            
    def _empty_seq(self, i):
        k = self._ws(i+1)
        if (self._cfg[i] in ":|") and (self._cfg[k] in "|;"):
            return k
        else:
            return i

    def _seq(self, i):
        elems = []
        while i < len(self._cfg):
            i = self._ws(i)
            j, name = self._id(i)
            if j > i:
                if name in self._toks:
                    if name in self._sym_toks:
                        elems.append(Sym_Term(name))
                    else:
                        elems.append(Term(name))
                else:
                    elems.append(Non_Term_Ref(name))
                i = j
                continue

            m = _RE_TOKEN.match(self._cfg, i)
            if m:
                name = m.group(1)
                elems.append(Term(name))
                i = m.end(0)
                continue
            

            if self._cfg[i] in "|;":
                return i, elems


    def _option(self, i):
        m = _RE_OPTIONS.match(self._cfg, i)
        if m:
            return m.end(0), None
        return i, None



def parse(lex, cfg):
    return _Parser().parse(lex, cfg)



if __name__ == "__main__":
    import sys
    import Lexer
    lex = Lexer.parse(open(sys.argv[2],"r").read())
    print parse(lex, open(sys.argv[1], "r").read())
