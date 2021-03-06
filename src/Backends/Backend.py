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


import sys, time
import Accent
import Utils
import traceback

class Simple:
    def __init__(self, sin):
        self._sin = sin
        self._cfg = sin.cfg.clone()


    def run(self, parserp, depth, wgt=None, duration=None):
        rec = 0
        timer = False
        if duration is not None:
            timer = True

        start = time.time()
        while ((not timer) or (not Utils.time_elapsed(start, duration))):
            sys.stdout.write(".\n=====>\n")
            sys.stdout.flush()
            try:
                t2 = time.time()
                s = self.next(depth, wgt)
                t3 = time.time()
                out = Accent.run(parserp, s)
                t4 = time.time()
                if Accent.was_ambiguous(out):
                    print "\n==> sentence[gen=%.6f parse=%.6f (secs)]: %s" % \
                                    ((t3-t2), (t4-t3), s)
                    print
                    print "".join(out)
                    return True, s, out
            except RuntimeError as err:
                if "maximum recursion depth exceeded" in err.message:
                    rec += 1
                    sys.stderr.write("\nr:%s\n" % rec)
                    sys.stderr.flush()
                    # useful to know what dynamic3 found before hitting recursion
                    if self._sin.backend in ['dynamic3']:
                        print "======="
                        for rule in self._cfg.rules:
                            if rule.finite_depth is not None:
                                print "[%s], %s" % (rule.finite_depth, rule)

                else:
                    # track other errors
                    print "error: \n"
                    print traceback.format_exc()
                    sys.exit(2)

        return False, None, None
