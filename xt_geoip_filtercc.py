#!/usr/bin/python2

"""
Filter GeoIP countries from a GeoLite2 database.

"""


from __future__ import with_statement

import sys

import fileinput
import csv



def main():
  filterCC = set([s.strip() for s in sys.argv[1].split(',')])
  sys.argv = [sys.argv[0]] + sys.argv[2:]   # needed for fileinput

  print >> sys.stderr, "Filter CC (%s)" % (list(filterCC))

  reader = csv.reader(fileinput.input())
  for ll in reader:
    assert len(ll) == 6
    if ll[4] in filterCC:
      print >> sys.stdout, ",".join(["\"%s\"" %s for s in ll])



if '__main__' == __name__:
  main()


