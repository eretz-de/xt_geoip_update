#!/usr/bin/python2

"""
Merges GeoIP ranges from a GeoLite2 database.

Because the original database works with subnets but we
expect a ranges with a start and end ip address, we can
merge sometimes ranges that are contigous.

For the complete database from 2019-09-01 this reduces
the CSV from 433401 lines to 211443 lines.
"""


from __future__ import with_statement

import sys

import fileinput
import csv



def main():
  cnt4In, cnt6In, cnt4Out, cnt6Out = 0, 0, 0, 0
  lastll, lastNumEnd, lastCC = None, None, None
  reader = csv.reader(fileinput.input())
  for ll in reader:
    #ll = line.strip().split(',')
    assert len(ll) == 6
    ipStart, ipEnd, numStart, numEnd, cc, country = ll
    numStart, numEnd = long(numStart.strip('"')), long(numEnd.strip('"'))
    assert ll[2] == "%s" % numStart, "number conversion failed, signed problem?"
    assert ll[3] == "%s" % numEnd, "number conversion failed, signed problem?"

    if lastNumEnd is not None:
      assert lastNumEnd <= numEnd, "wrong sort order"
      if numStart < lastNumEnd+1:
        print >> sys.stderr, "Warning: overlapping ranges, check your data", lastll, ll
        sys.stderr.flush()

    if ':' in ipStart:
      cnt6In += 1
    else:
      cnt4In += 1
    if lastCC == cc and numStart <= lastNumEnd+1:
      # merge range
      #print >> sys.stderr, "merge two ranges ", lastll, ll
      assert ll[5] == lastll[5]
      lastll = lastll[0], ll[1], lastll[2], ll[3], ll[4], ll[5]
    else:
      if lastll:
        print >> sys.stdout, ",".join(["\"%s\"" %s for s in lastll])
        if ':' in lastll[0]:
          cnt6Out += 1
        else:
          cnt4Out += 1
      lastll = ll
    lastNumEnd = numEnd
    lastCC = cc
  if lastll:
    print >> sys.stdout, ",".join(["\"%s\"" %s for s in lastll])
    if ':' in lastll[0]:
      cnt6Out += 1
    else:
      cnt4Out += 1

  sys.stdout.flush()
  print >> sys.stderr, "Stats: IPv4 read %(cnt4In)d ranges, wrote %(cnt4Out)d; IPv6 read %(cnt6In)d ranges, wrote %(cnt6Out)d" % locals()
  sys.stderr.flush()



if '__main__' == __name__:
  main()


