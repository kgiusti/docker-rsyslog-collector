%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/%{name}-%{version}
%if 0%{?rhel} >= 7
%global want_hiredis 0
%global want_mongodb 0
%global want_rabbitmq 0
%else
%global want_hiredis 1
%global want_mongodb 1
%global want_rabbitmq 1
%endif
# we provide these libraries privately, for use by the omamqp1 module, so
# don't want the automatic dependency generator creating a runtime dependency
# on the qpid-proton-c package, or advertising that this package provides
# qpid proton
%define __requires_exclude ^libqpid.*$
%define __provides_exclude ^libqpid.*$

Summary: Rsyslog AMQP v1 output module
Name: rsyslog-omamqp1
Version: 7.4.7
Release: 12%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/rsyslog-%{version}.tar.gz
Source2: rsyslog.conf
Source3: rsyslog.sysconfig
Source4: rsyslog.log
Source5: rsyslog-omamqp1.tar.gz
# tweak the upstream service file to honour configuration from /etc/sysconfig/rsyslog
Patch0: rsyslog-7.4.1-sd-service.patch
Patch1: rsyslog-7.2.2-manpage-dbg-mode.patch
# prevent modification of trusted properties (proposed upstream)
Patch2: rsyslog-7.2.1-msg_c_nonoverwrite_merge.patch
# sent upstream
Patch5: rsyslog-7.4.7-bz1030044-remove-ads.patch
# merged upstream
Patch6: rsyslog-7.4.7-numeric-uid.patch
# adapted from http://git.adiscon.com/?p=rsyslog.git;a=commitdiff;h=16207e3d55ac6bb15af6d50791d2c7462816de57
Patch7: rsyslog-7.4.7-omelasticsearch-atomic-inst.patch
Patch8: rsyslog-7.4.7-bz1052266-dont-link-libee.patch
Patch9: rsyslog-7.4.7-bz1054171-omjournal-warning.patch
Patch10: rsyslog-7.4.7-bz1038136-imjournal-message-loss.patch
Patch11: rsyslog-7.4.7-bz1142373-cve-2014-3634.patch
Patch12: rsyslog-7.4.7-rhbz1151037-add-mmcount.patch
Patch13: rsyslog-7.4.7-rhbz743890-imjournal-sanitize-msgs.patch
Patch14: rsyslog-7.4.7-rhbz1184410-imuxsock-create-path.patch
Patch15: rsyslog-7.4.7-rhbz1202489-path-creation-race.patch
Patch16: rsyslog-7.4.7-rhbz1238713-html-docs.patch
Patch17: rsyslog-7.4.7-rhbz1078878-division-by-zero.patch
Patch18: rsyslog-7.4.7-rhbz1143846-clarify-SysSock.Use.patch
Patch19: rsyslog-7.4.7-rhbz1151041-imuxsock-socket-limit.patch
Patch20: rsyslog-7.4.7-rhbz1101602-imjournal-zero-bytes.patch
Patch21: rsyslog-7.4.7-rhbz1188503-imjournal-default-tag.patch
Patch22: rsyslog-7.4.7-rhbz1184402-imuxsock-hostname.patch
Patch23: rsyslog-7.4.7-bz1254511-ppc64le_bug.patch

BuildRequires: bison
BuildRequires: flex
BuildRequires: json-c-devel
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
# make sure systemd is in a version that isn't affected by rhbz#974132
BuildRequires: systemd-devel >= 204-8
BuildRequires: zlib-devel
BuildRequires: qpid-proton-c-devel

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libgcrypt-devel

%package doc
Summary: HTML Documentation for rsyslog
Group: Documentation

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libee-devel liblognorm-devel

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql >= 4.0
BuildRequires: mysql-devel >= 4.0

%if %{want_mongodb}
%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%if %{want_rabbitmq}
%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2
%endif

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.0.3
BuildRequires: librelp-devel >= 1.0.3

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel

%description
Rsyslog-omamqp1 is an AMQP v1 output module for rsyslog that uses QPID Proton
as the implementation.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%description doc
This subpackage contains documentation for rsyslog.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%if %{want_mongodb}
%description mongodb
The rsyslog-mongodb package contains a dynamic shared object that will add
MongoDB database support to rsyslog.
%endif

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%if %{want_rabbitmq}
%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.
%endif

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%prep
%setup -q -n rsyslog-%{version}
%setup -q -n rsyslog-%{version} -T -D -a 5
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%build
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DSYSLOGD_PIDNAME=\\\"syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS=-L%{_libdir}
%endif
%configure \
	--prefix=/usr \
	--disable-static \
	--disable-testbench \
	--enable-elasticsearch \
	--enable-gnutls \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp \
	--enable-libdbi \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mysql \
%if %{want_hiredis}
	--enable-omhiredis \
%endif
	--enable-omjournal \
%if %{want_mongodb}
	--enable-ommongodb \
%endif
	--enable-omprog \
%if %{want_rabbitmq}
	--enable-omrabbitmq \
%endif
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmrfc3164sd \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \

./config.status --file=plugins/omamqp1/Makefile
PKG_CONFIG=${PKG_CONFIG:-pkg-config}
PROTON_CFLAGS=`$PKG_CONFIG --cflags "libqpid-proton >= 0.9" 2>/dev/null`
PROTON_LIBS=`$PKG_CONFIG --libs "libqpid-proton >= 0.9" 2>/dev/null`
sed -i -e "s/@PROTON_CFLAGS@/${PROTON_CFLAGS}/g" \
    -e "s/@PROTON_LIBS@/${PROTON_LIBS}/g" \
    plugins/omamqp1/Makefile
LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C plugins/omamqp1

%install
LD_RUN_PATH=%{_libdir}/rsyslog/qpid-proton-c make -C plugins/omamqp1 DESTDIR=%{buildroot} install

# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# private version of qpid
install -d -m 755 %{buildroot}%{_libdir}/rsyslog/qpid-proton-c
install -p -m 755 %{_libdir}/libqpid* %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/
rm -f %{buildroot}%{_libdir}/rsyslog/qpid-proton-c/*.so

%files
%defattr(-,root,root,-)
# plugins
%{_libdir}/rsyslog/omamqp1.so
%{_libdir}/rsyslog/qpid-proton-c

%changelog
* Mon Feb  1 2016 Rich Megginson <rmeggins@redhat.com> 7.4.7-12
- initial commit - hacked rsyslog.spec
