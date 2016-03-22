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

import Min1, Min1a
import Min2, Min2a
import Min3, Min3a
import Min4, Min5, Min6
import MinAD

MINIMISERS = {
    'min1': Min1.Min1,
    'min2': Min2.Min2,
    'min2a': Min2a.Min2a,
    'min3': Min3.Min3,
    'min3a': Min3a.Min3a,
    'min4': Min4.Min4,
    'min5': Min5.Min5,
    'min6': Min6.Min6,
    'minad': MinAD.MinAD,
    'min1a': Min1a.Min1a,
}
