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

