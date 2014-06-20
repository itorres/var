#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import sys


dst=""
tab = {
  167: 243, # o acute
  168: 242, # o grave
  171: 239, # i diaeresis ï 426
  172: 238, # i acute í 
  173: 237, # i grave ì
  177: 233, # e acute è
  178: 232, # e grave
  179: 231, # ç
  185: 224, # a grave
  197: 210, # O grave

  220: 169, # copyright
  114: 183, # middle dot
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
  if len(sys.argv) > 3:
      z = a + int(sys.argv[3])
  orig = f.read()[a:z]
  for i,c in enumerate(orig):
    n = ord(c)
    dn=n+31
    if n == 32:
        continue # Ignore redundant blank spaces
    if n > 57313 and n < 57363:
      dn = n - 57313
    elif n > 155 and n<185: # Arbitrary limits
        dn = 255-(n-155)
    elif n in tab:
      dn=tab[n]
    dc = unichr(dn)

    if last < 48 and dn == 41: # if last character was a symbol and I'm a middle dot
        dc = unichr(10) # newline

    if debug:
        print('%4d: Orig: %s(%d)\tDest: %s(%d)' % (i, c, n, dc, dn))
    dst = dst + dc
    last = dn

print(dst)
