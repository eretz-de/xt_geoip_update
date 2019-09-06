#!/usr/bin/python2

"""
Merges GeoIP countries from a GeoLite2 database.

A later use of xt_geoip_mergerange.py may be able to reduce
the memory requirement when the new country has more
contiguous ranges.
"""


from __future__ import with_statement

import sys

import fileinput
import csv



def main():
  newCountry = sys.argv[1]
  newCC = sys.argv[2]
  oldCCs = set([s.strip() for s in sys.argv[3].split(',')])
  sys.argv = [sys.argv[0]] + sys.argv[4:]   # needed for fileinput

  print >> sys.stderr, "Replacing CC (%s) with %s (%s)" % (list(oldCCs), newCC, newCountry)

  reader = csv.reader(fileinput.input())
  for ll in reader:
    assert len(ll) == 6
    if ll[4] in oldCCs:
      ll[4] = newCC
      ll[5] = newCountry
    print >> sys.stdout, ",".join(["\"%s\"" %s for s in ll])



if '__main__' == __name__:
  main()


