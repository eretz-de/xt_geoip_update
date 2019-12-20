#!/usr/bin/python2

"""
Filter GeoIP countries from a GeoLite2 database.

"""


from __future__ import with_statement
from __future__ import print_function   # prepare for python3, since Python3.3 we would have print("", flush=True)

import sys

import fileinput
import csv



def main():
  filterCC = set([s.strip() for s in sys.argv[1].split(',')])
  sys.argv = [sys.argv[0]] + sys.argv[2:]   # needed for fileinput

  print("Filter CC (%s)" % (list(filterCC)), file=sys.stderr)
  sys.stderr.flush()

  reader = csv.reader(fileinput.input())
  for ll in reader:
    assert len(ll) == 6
    if ll[4] in filterCC:
      print(",".join(["\"%s\"" %s for s in ll]))



if '__main__' == __name__:
  main()


