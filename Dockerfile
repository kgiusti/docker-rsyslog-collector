FROM centos:centos7
MAINTAINER The ViaQ Community <community@TBA>

EXPOSE 5141

ENV HOME=/opt/app-root/src \
    PATH=/opt/app-root/src/bin:/opt/app-root/bin:$PATH \
    SYSLOG_LISTEN_PORT=5141 \
    AMQP_HOST=viaq-qpid-router \
    AMQP_PORT=5672

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    curl https://copr.fedorainfracloud.org/coprs/rmeggins/rsyslog/repo/epel-7/rmeggins-rsyslog-epel-7.repo > /etc/yum.repos.d/rmeggins-rsyslog-epel-7.repo && \
    yum install -y rsyslog rsyslog-gssapi qpid-proton-c \
    rsyslog-mmjsonparse rsyslog-mmsnmptrapd && \
    yum clean all

ADD rsyslog.conf /etc/rsyslog.conf
ADD rsyslog.d/* /etc/rsyslog.d/
ADD run.sh /usr/sbin/
WORKDIR /var/lib/rsyslog

CMD /usr/sbin/run.sh
