# xt_geoip_update
Update xt_geoip database for netfilter

This repository defines a docker image that can be used to update the current database for the geoip netfilter module. For this it uses the Docker image from https://github.com/sander1/docker-xtables that itself uses [https://github.com/mschmitt/GeoLite2xtables](https://github.com/mschmitt/GeoLite2xtables).


## Motivation

Because these tools need to convert the new datasource to the old format there are too many IP ranges defined. This stems from the fact, that the new database uses subnets but the old database uses ranges with start and end ip addresses which is also used for the binary files created for the Netfilter module.

But subnetting is not always able to concatenate two contigous IP ranges:

    192.168.1.0/24
    192.168.2.0/24
    192.168.3.0/24

can be merged to

    192.168.1.0/24
    192.168.2.0/23

But with start and end address it would be simply:

    192.168.1.0 - 192.168.3.255

## Tools

### xt_geoip_mergerange.py

This reads from STDIN or the given file and writes the merged ranges to STDOUT.

It expects the input to be sorted by the IP address.


### xt_geoip_filtercc.py

This reads from STDIN or the given file and writes the ranges from the given countries to STDOUT.

Give the countries to select as comma separated list of country codes as first argument.


### xt_geoip_mergecc.py

This reads from STDIN or the given file and writes the ranges from to STDOUT but modifies the given countries.

You can use this to create a new country that contains the ranges from multiple other countries. Because of the range merging from [xt_geoip_mergerange.py](#xt_geoip_mergerangepy) this new country may have fewer ranges than the sum of the original countries.

You need to give the new country name as first argument (not really used), then the new country code not allowed to collide with existing codes and then the comma separated list of country codes to be merged.

The country codes `A[0-9]` are partially in use (for Satellite Provider), but other letter do not use digits, therefore using a digit in the country codes should make them unique.


### Example

Merge the full database:

    ./xt_geoip_mergerange.py ./GeoIP-legacy.csv > ./GeoIP-merged.csv

Create two new countries for optimized search in Netfilter:

    xt_geoip_filtercc.py "NL,DK,NO,AT,A1,A2" /xt_build/GeoIP-merged.csv |
      xt_geoip_mergecc.py "Next vacations" "Y0" "NL,DK,NO,SE,AT" |
      xt_geoip_mergecc.py "Evil Hackers" "X0" "A1,A2" |
      xt_geoip_mergerange.py > /xt_build/special-countries-merged.csv

Now you can use this with iptables:

    iptables -A INPUT -m geoip --source-country X0 -j DROP
    iptables -A INPUT -p icmp -m icmp --icmp-type 8 -m geoip --source-country Y0 -j ACCEPT


## Docker image

You can use the provided docker image to download/update, convert and optimize the GeoIP database. Call it like this:

    docker run --rm -v /usr/share/xt_geoip:/xt_build eretz/xt_geoip_update

This will replace the files in /usr/share/xt_geoip (the default location used by the xt_geoip module).


To create special countries for your local firewall you can place a script `xt_rebuild_local.sh` into the /usr/share/xt_geoip folder that will be called by the docker image. This script can use the `GeoIP-merged.csv` that already exists. Check the following example:

    #!/bin/bash

    set -e

    BUILDDIR="$(dirname "$0")"

    cd "$BUILDDIR"

    # create our own countries because of the merging they are smaller than the sum
    xt_geoip_filtercc.py "NL,DK,NO,AT,A1,A2" ./GeoIP-merged.csv |
      xt_geoip_mergecc.py "Next vacations" "Y0" "DE,NL,DK,NO,SE,AT,CH" |
      xt_geoip_mergecc.py "Evil Hackers" "X0" "A1,A2" |
      xt_geoip_mergerange.py > ./special-countries-merged.csv

    # remove old data and hope that we can recreate them
    rm -f dummy [LB]E/[XY][0-9].iv[46]

    # build files for these special countries
    /usr/libexec/xtables-addons/xt_geoip_build -D "$BUILDDIR" "$BUILDDIR/special-countries-merged.csv"

Do not forget to chmod the script as executable:

    chmod +rx /usr/share/xt_geoip/xt_rebuild_local.sh


### As cron job

If you call the docker image as a monthly cron job to update the xt_geoip database you should update the docker image before you run it. A script to call via cron would be:

    #!/bin/bash

    # update image to avoid using an old one from the cache
    docker pull eretz/xt_geoip_update

    # use snapper to make snapshots before and after the update

    /usr/bin/snapper --config root create \
      --description "$0: download and convert GeoLite2xtables" \
      --cleanup-algorithm number \
      --command "docker run --rm -v /usr/share/xt_geoip:/xt_build eretz/xt_geoip_update"

This cron-job uses *snapper* to make a snapshot before and after the update.
