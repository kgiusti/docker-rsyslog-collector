# How to use this spec file

Grab the el7 version of the rsyslog spec and sources::

    $ wget http://vault.centos.org/centos/7/os/Source/SPackages/rsyslog-7.4.7-12.el7.src.rpm
    $ rpm2cpio rsyslog-7.4.7-12.el7.src.rpm | cpio -id
    $ builddir=`pwd`

Create the rsyslog-omamqp1.tar.gz file containing only the plugin source code.
For example, if you have a local git repo with the source code in
$HOME/rsyslog::

    $ cd $HOME/rsyslog
    $ tar cfz $builddir/rsyslog-omamqp1.tar.gz plugins/omamqp1

Build the rsyslog-omamqp1 srpm with the spec file::

    $ rpmbuild --define '_topdir .' --define '_sourcedir .' \
        --define 'dist .el7' -bs rsyslog-omamqp1.spec

Now you can use the SRPMS/rsyslog-omamqp1-7.4.7-12.el7.src.rpm to build the plugin.

mock::

    mock -r epel-7-x86_64 SRPMS/rsyslog-omamqp1-7.4.7-12.el7.src.rpm

or copr e.g. https://copr.fedorainfracloud.org/coprs/rmeggins/rsyslog-omamqp1/

NOTE: The spec file bundles qpid-proton-c in a private location.  If and when
qpid-proton-c is available as a regular el7 package, remove the hacks from the
spec file and make qpid-proton-c a regular dependency.
