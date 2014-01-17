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


import Purerandom, Random2, Random3, Random4
import Dynamic1, Dynamic2, Dynamic3, Dynamic4, Dynamic5, Dynamic6, Dynamic7
import Dynamic8

BACKENDS = {
  "purerandom"  : Purerandom.Calc,
  "random2"  : Random2.Calc,
  "random3"  : Random3.Calc,
  "random4"  : Random4.Calc,
  "dynamic1" : Dynamic1.Calc,
  "dynamic2" : Dynamic2.Calc,
  "dynamic3" : Dynamic3.Calc,
  "dynamic4" : Dynamic4.Calc,
  "dynamic5" : Dynamic5.Calc,
  "dynamic6" : Dynamic6.Calc,
  "dynamic7" : Dynamic7.Calc,
  "dynamic8" : Dynamic8.Calc
}
