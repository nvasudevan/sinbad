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

import Dynamic1, Dynamic1rws
import Dynamic2, Dynamic2rws
import Dynamic3

import Dynamic2rwsMin, Dynamic1rwsMin

import Dynamic12, Dynamic13
import Dynamic1m, Dynamic3m
import Dynamic11m, Dynamic12m

import Dynamic2a, Dynamic4a
import Dynamic5, Dynamic6, Dynamic7a
import Dynamic8, Dynamic9, Dynamic10, Dynamic11

BACKENDS = {
  "purerandom" : Purerandom.Calc,
  "random2"    : Random2.Calc,
  "random3"    : Random3.Calc,
  "random4"    : Random4.Calc,
  "dynamic1"   : Dynamic1.Calc,
  "dynamic2"   : Dynamic2.Calc,
  "dynamic3"   : Dynamic3.Calc,
  "dynamic6"   : Dynamic6.Calc,
  "dynamic1m"  : Dynamic1m.Calc,
  "dynamic3m"  : Dynamic3m.Calc,
  "dynamic13"  : Dynamic13.Calc,
}

WGTBACKENDS = {
  "dynamic1rws"    : Dynamic1rws.Calc,
  "dynamic2rws"    : Dynamic2rws.Calc,
  "dynamic11"      : Dynamic11.Calc,
  "dynamic12"      : Dynamic12.Calc,
  "dynamic11m"     : Dynamic11m.Calc,
  "dynamic12m"     : Dynamic12m.Calc,
}

MINIMISER_BACKENDS = {
  "dynamic2rwsMin" : Dynamic2rwsMin.Calc,
  "dynamic1rwsMin" : Dynamic1rwsMin.Calc,
}

EXPERIMENTAL_BACKENDS = {
  "dynamic2a" : Dynamic2a.Calc,
  "dynamic4a" : Dynamic4a.Calc,
  "dynamic5"  : Dynamic5.Calc,
  "dynamic7a" : Dynamic7a.Calc,
  "dynamic8"  : Dynamic8.Calc,
  "dynamic9"  : Dynamic9.Calc,
  "dynamic10" : Dynamic10.Calc,
}
