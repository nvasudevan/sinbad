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


import os, subprocess
import tempfile, sys
import Lexer


class AmbiDexter:

    def __init__(self, jarp, opts=None, ws=False, heap='1g'):
        self.jarp = jarp
        self.opts = opts
        self.ws = ws
        self.heap = heap
        self.javacmd = ['/usr/bin/java', '-Xss8m', '-Xmx%s' % (self.heap),\
                        '-jar', self.jarp]


    def to_yacc(self, gp):
        """ convert the grammar format from ACCENT to YACC """
        d, _ = os.path.split(gp)
        tp = tempfile.mktemp('.y', dir=d)
        with open(tp, 'w') as tf:
            with open(gp) as gf:
                for l in gf:
                    if l.startswith('%token'):
                        _l = l.replace(',', '').replace(';', '')
                        tf.write(_l)
                    else:
                        if l.startswith('%nodefault'):
                            _l = l.replace('%nodefault', '%%')
                            tf.write(_l)
                        else:
                            tf.write(l)

        return tp


    def run(self, gp, opts, duration):
        cmd = ['/usr/bin/timeout', duration] + self.javacmd + opts
        p = subprocess.Popen(cmd + [self.to_yacc(gp)], stdout=subprocess.PIPE)
        out, err =  p.communicate()
        r = p.returncode
        return out, err, r


    def convert_sen(self, sen, lp):
        """ sen contains symbolic tokens, convert to 'actual' tokens using
            the lex
        """
        lex = Lexer.parse(open(lp, "r").read())
        _sen = []
        for tok in sen.split():
            if tok in lex.keys():
                _sen.append(lex[tok])
            else:
                # single char quoted tokens
                _sen.append(tok.replace("'", ""))

        if "WS" in lex.keys():
            return "".join(_sen)
        else:
            # the origingal grammar had WS rule but not anymore.
            if self.ws:
                return "".join(_sen)

            return " ".join(_sen)


    def ambiguous(self, gp, lp, duration='30', xtra_opts=[]):
        _opts = self.opts + xtra_opts
        print "\n=> check ambiguity on %s with opts %s" % (gp, _opts)
        out, err, r = self.run(gp, _opts, duration)
        if r == 0:
            for l in out.split('\n'):
                if l.startswith('ambiguous sentence:'):
                    sen = l.replace('ambiguous sentence: ', '')
                    return sen, self.convert_sen(sen, lp)

        # timeout throws return code 124
        if ((r != 0) and (r != 124)):
            msg = "AmbiDexter failed for grammar: %s " % gp
            print "%s\n---\nout:%s\n err:%s" % (msg, out, err)
            sys.exit(1)

        return None, None


    def filter(self, gp, duration='30', xtra_opts=[]):
        _opts = self.opts + xtra_opts
        print "\n=> apply filter on %s with opts %s" % (gp, _opts)
        out, err, r = self.run(gp, _opts, duration)
        if r == 0:
            for l in out.split('\n'):
                if l.startswith('Exporting grammar to'):
                    fltrp = l.replace('Exporting grammar to ', '')
                    print "fltrp: " , fltrp
                    return fltrp

        if ((r != 0) and (r != 124)):
            msg = "AmbiDexter failed for grammar: %s " % gp
            print "%s\n---\nout:%s\n err:%s" % (msg, out, err)
            sys.exit(1)

        return None


if __name__ == "__main__":
    import sys
    gp = sys.argv[1]
    print gp
    #x, _ = ambiguous(gp, './AmbiDexter.jar', ['-q', '-pg', '-ik', '0'])
    x, _ = filter(gp, './AmbiDexter.jar', ['-q', '-pg', '-h', '-slr1', '-oa']) 
    print x 

