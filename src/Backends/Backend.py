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


    def run(self, depth, wgt=None, duration=None):
        recursion = 0
        timer = False
        if duration is not None:
            timer = True

        start = time.time()
        while ((not timer) or (not Utils.time_elapsed(start, duration))):
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                t2 = time.time()
                s = self.next(depth, wgt)
                t3 = time.time()
                out = Accent.run(self._sin.parser, s)
                t4 = time.time()
                if Accent.was_ambiguous(out):
                    print "sentence[gen=%.6f parse=%.6f (secs)]: %s" % \
                                    ((t3-t2), (t4-t3), s)
                    print
                    print "".join(out)
                    return True, s, out
            except RuntimeError as err:
                if "maximum recursion depth exceeded" in err.message:
                    recursion += 1 
                    sys.stdout.write("r:%s" % str(recursion))
                    sys.stdout.flush()
                    sys.exit(1)
                else:
                    print "error: \n"
                    print traceback.format_exc()
                    sys.exit(2)

        return False, None, None
