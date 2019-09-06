#!/bin/bash

export PATH=$PATH:/opt/GeoLite2xtables/

set -e

cd /xt_build


# call script from https://github.com/sander1/docker-xtables/blob/master/xt_build.sh
xt_build.sh

# merge contiguous ranges should save about 50% of lines
xt_geoip_mergerange.py /xt_build/GeoIP-legacy.csv > /xt_build/GeoIP-merged.csv

# build files for these countries
/usr/libexec/xtables-addons/xt_geoip_build -D /xt_build /xt_build/GeoIP-merged.csv


if [ -x /xt_build/xt_rebuild_local.sh ]; then
  /xt_build/xt_rebuild_local.sh 
fi

