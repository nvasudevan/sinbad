
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



from Backends import Dynamic1, Dynamic2, Dynamic3
from Backends import Dynamic11
from Backends import Dynamic8, Dynamic9, Dynamic10


BACKENDS = {
  "dynamic1"   : Dynamic1.Calc,
  "dynamic2"   : Dynamic2.Calc,
  "dynamic3"   : Dynamic3.Calc,
}

WGTBACKENDS = {
  "dynamic11"   : Dynamic11.Calc,
}

EXPERIMENTAL_BACKENDS = {
  "dynamic8"  : Dynamic8.Calc,
  "dynamic9"  : Dynamic9.Calc,
  "dynamic10" : Dynamic10.Calc,
}