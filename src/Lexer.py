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


import re



_RE_DELIM  = re.compile(r"%%.*")
_RE_LEX    = re.compile("(.*?)\s*\{.*?}")
_RE_LEX_ID = re.compile("(.*?)\s*\{\s*return\s*(.*?)\s*;\s*\}")



class _Parser:
    def parse(self, lexer):
        self._lexer = lexer

        toks = {}
        i = 0
        while i < len(lexer):
            i = self._ws(i)

            m = _RE_LEX_ID.match(lexer, i)
            if m:
                tok_re = self._dequote(m.group(1))
                tok_id = self._dequote(m.group(2))
                toks[tok_id] = tok_re
                i = m.end(0)
                continue

            m = _RE_LEX.match(lexer, i)
            if m:
                i = m.end(0)
                continue

            if lexer.startswith("%{", i):
                i += 2
                while not lexer.startswith("%}", i):
                    i += 1
                i += 2
                continue

            m = _RE_DELIM.match(lexer, i)
            if m:
                i = m.end(0)
                continue

        return toks


    def _ws(self, i):
        while i < len(self._lexer) and self._lexer[i] in " \n\r\t":
            i += 1
        return i


    def _dequote(self, s):
        if (s.startswith("\"") and s.endswith("\"")) \
          or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        return s


def parse(lexer):
    return _Parser().parse(lexer)



if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        toks = parse(open(p, "r").read())
        print toks.keys()
