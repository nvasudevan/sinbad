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
import Dynamic2, Dynamic2rws, Dynamic2fd
import Dynamic3
import Dynamic4

import Dynamic1rwsMin
import Dynamic2rwsMin, Dynamic2fdMin

import Dynamic1m, Dynamic2m, Dynamic3m, Dynamic2rwsm
import Dynamic11m

import Dynamic2a, Dynamic4a, Dynamic4b
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
  "dynamic4"   : Dynamic4.Calc,
  "dynamic6"   : Dynamic6.Calc,
  "dynamic1m"  : Dynamic1m.Calc,
  "dynamic2m"  : Dynamic2m.Calc,
  "dynamic3m"  : Dynamic3m.Calc,
}

WGTBACKENDS = {
  "dynamic1rws" : Dynamic1rws.Calc,
  "dynamic2rws" : Dynamic2rws.Calc,
  "dynamic2rwsm" : Dynamic2rwsm.Calc,
  "dynamic2fd"  : Dynamic2fd.Calc,
  "dynamic11"   : Dynamic11.Calc,
}

MINIMISER_BACKENDS = {
  "dynamic2rwsMin" : Dynamic2rwsMin.Calc,
  "dynamic1rwsMin" : Dynamic1rwsMin.Calc,
  "dynamic2fdMin"  : Dynamic2fdMin.Calc,
  "dynamic11m"     : Dynamic11m.Calc,
}

EXPERIMENTAL_BACKENDS = {
  "dynamic2a" : Dynamic2a.Calc,
  "dynamic4a" : Dynamic4a.Calc,
  "dynamic4b" : Dynamic4b.Calc,
  "dynamic5"  : Dynamic5.Calc,
  "dynamic7a" : Dynamic7a.Calc,
  "dynamic8"  : Dynamic8.Calc,
  "dynamic9"  : Dynamic9.Calc,
  "dynamic10" : Dynamic10.Calc,
}
