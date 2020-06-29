FROM sander1/xtables_geoip:latest

# FROM alpine:3.8.4


WORKDIR /opt

RUN \
  apk add --no-cache --update \
    python2=2.7.15-r3

COPY ./xt_rebuild.sh ./xt_geoip_*.py /opt/GeoLite2xtables/

RUN chmod +x /opt/GeoLite2xtables/xt_rebuild.sh /opt/GeoLite2xtables/xt_geoip_*.py

VOLUME /xt_build

ENTRYPOINT ["/opt/GeoLite2xtables/xt_rebuild.sh"]
