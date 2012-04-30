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


def compile(old_gp, old_lp):
    td = tempfile.mkdtemp()

    # Accent and lex doen't allow us to specify *where* the output files
    # it generates should be put. We therefore have to rely on hackery.

    new_gp = os.path.join(td, os.path.split(old_gp)[1])
    r = subprocess.call(["cp", old_gp, new_gp])
    if r != 0:
        error("Copy failed.\n", r)
    r = os.system("cd %s ; ${ACCENT_DIR}/accent/accent %s" % (td, new_gp))
    if r != 0:
        error("accent failed.\n", r)

    new_lp = os.path.join(td, os.path.split(old_lp)[1])
    r = subprocess.call(["cp", old_lp, new_lp])
    if r != 0:
        error("Copy failed.\n", r)
    r = os.system("cd %s ; flex %s" % (td, new_lp))
    if r != 0:
        error("lex failed.\n", r)

    parser = os.path.join(td, "parser")
    r = os.system(" ".join(["cc -w", "-o", parser, \
      os.path.join(td, "yygrammar.c"), os.path.join(td, "lex.yy.c"), \
      "${ACCENT_DIR}/exmplaccent/auxil.c", "${ACCENT_DIR}/entire/entire.c"]))
    if r != 0:
        error("cc failed.\n", r)

    return parser


def run(parser, s):

    p = subprocess.Popen(parser, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(s)
    return "".join(out[0])


def was_ambiguous(out):
    if "GRAMMAR DEBUG INFORMATION" in out:
        return True
    return False