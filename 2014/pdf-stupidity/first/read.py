#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import sys


dst=""
tab = {
  185: 224, # a grave
  178: 232, # e grave
  57517: 237, # i acute
  167: 243, # o acute
  168: 242, # o grave
  57503: 252, # u diaeresis
  114: 183, # middle dot
  #114: 10, # newline
  32: 32,
  57364: 10,
  57365: 10,
  57366: 10,
  57367: 10,
  57368: 10,
  57369: 10,
}

last = 0
debug = False
with codecs.open(sys.argv[1],encoding='utf-8') as f:
  # orig = f.read()
  a=0; z=-1
  if len(sys.argv) > 2:
      debug=True
      a = int(sys.argv[2])
      z = a + 40
  orig = f.read()[a:z]
  for i,c in enumerate(orig):
    n = ord(c)
    dn=n+31
    if n > 57313 and n < 57363:
      dn = n - 57313
    elif n in tab:
      dn=tab[n]
    dc = unichr(dn)
    if last in (46,41) and dn == 183: # if last character was a symbol and I'm a middle dot
        dc = unichr(10) + unichr(dn) # prefix a newline
    if debug:
        print('%4d: Orig: %s(%d)\tDest: %s(%d)' % (i, c, n, dc, dn))
    dst = dst + dc
    last = dn

print(dst)
