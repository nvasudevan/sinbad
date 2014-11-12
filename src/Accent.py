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


import os, subprocess, tempfile
import Utils
import sys


def compile(old_gp, old_lp):
    # We do all the icky stuff in a temporary directory.
    td = tempfile.mkdtemp()

    new_gp = os.path.join(td, os.path.split(old_gp)[1])
    r = subprocess.call(["cp", old_gp, new_gp])
    if r != 0:
        Utils.error("Copy failed.\n", r)
    new_lp = os.path.join(td, os.path.split(old_lp)[1])
    r = subprocess.call(["cp", old_lp, new_lp])
    if r != 0:
        Utils.error("Copy failed.\n", r)

    # Accent and lex doen't allow us to specify *where* the output files
    # it generates should be put. We therefore temporarily chdir to 'td'.
    cwd = os.getcwd()
    os.chdir(td)

    # Accent

    r = os.system("${ACCENT_DIR}/accent/accent %s" % new_gp)
    if r != 0:
        Utils.error("accent failed.\n", r)

    # lex

    r = os.system("lex %s" % new_lp)
    if r != 0:
        Utils.error("lex failed.\n", r)

    # cc

    parser = os.path.join(td, "parser")
    r = subprocess.call(["cc", "-w", "-o", parser, \
      "yygrammar.c", "lex.yy.c", \
      os.path.expandvars("${ACCENT_DIR}/exmplaccent/auxil.c"), \
      os.path.expandvars("${ACCENT_DIR}/entire/entire.c")])
    if r != 0:
        Utils.error("cc failed.\n", r)

    os.chdir(cwd)

    return parser


def run(parser, s):

    p = subprocess.Popen(parser, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(s)
    if p.returncode != 0:
        print "sentence: " , s
        print "returncode: " , str(p.returncode)
        print "error: " , out
        sys.exit(1)

    return "".join(out[0])


def was_ambiguous(out):
    if "GRAMMAR DEBUG INFORMATION" in out:
        return True
    return False
