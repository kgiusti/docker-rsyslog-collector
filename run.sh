#!/bin/sh

set -e
set -x

SYSLOG_LISTEN_PORT=${SYSLOG_LISTEN_PORT:-5141}
AMQP_HOST=${AMQP_HOST:-bitscout-qpid-router}
AMQP_PORT=${AMQP_PORT:-5672}
AMQP_URL=${AMQP_URL:-amqp://$AMQP_HOST:$AMQP_PORT}

for file in /etc/rsyslog.conf /etc/rsyslog.d/*.conf /opt/app-root/etc/omamqp1.conf /etc/omamqp1.conf ; do
    if [ ! -f "$file" ] ; then continue ; fi
    sed -i -e "s/%SYSLOG_LISTEN_PORT%/$SYSLOG_LISTEN_PORT/g" \
        -e "s/%AMQP_HOST%/$AMQP_HOST/g" \
        -e "s/%AMQP_PORT%/$AMQP_PORT/g" \
        -e "s|%AMQP_URL%|$AMQP_URL|g" \
        "$file"
done
/usr/sbin/rsyslogd -d -n
