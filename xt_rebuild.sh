#!/bin/bash

PATH=$PATH:/opt/GeoLite2xtables/

set -e

cd /xt_build


# call script from https://github.com/sander1/docker-xtables/blob/master/xt_build.sh
xt_build.sh

# merge contiguous ranges should save about 50% of lines
xt_geoip_mergerange.py /xt_build/GeoIP-legacy.csv > /xt_build/GeoIP-merged.csv

# build files for these countries
/usr/libexec/xtables-addons/xt_geoip_build -D /xt_build /xt_build/GeoIP-merged.csv

# create our own countries because of the merging they are smaller than the sum
xt_geoip_filtercc.py "DE,NL,DK,NO,SE,AT,CH,CN,RU" /xt_build/GeoIP-merged.csv | 
  xt_geoip_mergecc.py "Nico Urlaub" "Y0" "DE,NL,DK,NO,SE,AT,CH" |
  xt_geoip_mergecc.py "Evil Hackers" "X0" "CN,RU" |
  xt_geoip_mergerange.py > /xt_build/special-countries-merged.csv

# remove old data and hope that we can recreate them
rm /xt_build/[LB]E/[XY][0-9].iv[46]

# build files for these special countries
/usr/libexec/xtables-addons/xt_geoip_build -D /xt_build /xt_build/special-countries-merged.csv
