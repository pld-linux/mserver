Summary:	Masq Dialer deamon.
Name:		mserver
Version:	0.5.5
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Vendor:		Chares P. Wright <cpwright@cpwright.com>
URL:		http://w3.cpwright.com
Source0:	ftp://ftp.cpwright.com/pub/mserver/c-%{name}-%{version}.tar.gz
Source1:	mserver.init
Source2:	mserver.pam
Prereq:		chkconfig
Requires:	rc-scripts >= 0.2.1
Requires:	ppp
Requires:	pam
BuildRequires:	pam-devel
Patch0:		mserver-config.patch
Patch1:		mserver-dial.patch
Patch2:		mserver-Makefile.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The masqdialer system will allow authorized LAN users to manipulate the
network interface (usually a modem) that gives the Internet access on a
Linux box without having to use telnet. It's based on a client/server
approach so any TCP/IP enabled system should be able to take advantage of
this server, if a client is written for it. Currently; Linux, Windows,
NetBSD, and any system with a Java implementation or Web Browser have
clients.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1

%build
LDFLAGS="-s"; export LDFLAGS
aclocal
autoconf
automake
autoheader
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{ppp,pam.d}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/{man5,man8}} \
	$RPM_BUILD_ROOT%{_datadir}/mserver

install mserver/mserver $RPM_BUILD_ROOT%{_sbindir}/mserver
install mchat/mchat $RPM_BUILD_ROOT%{_sbindir}/mchat
install authgen/authgen $RPM_BUILD_ROOT%{_sbindir}/authgen
install checkstat/findstat $RPM_BUILD_ROOT%{_sbindir}/findstat
install checkstat/checkstat $RPM_BUILD_ROOT%{_sbindir}/checkstat
install fakelink/linkcheck $RPM_BUILD_ROOT%{_sbindir}/fakelink
install fakelink/linkdown $RPM_BUILD_ROOT%{_sbindir}/linkdown
install fakelink/linkup $RPM_BUILD_ROOT%{_sbindir}/linkup

install mchat/mchat.8 $RPM_BUILD_ROOT%{_mandir}/man8/mchat.8
install docs/mserver.8 $RPM_BUILD_ROOT%{_mandir}/man8/mserver.8
install docs/mserver.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/mserver.conf.5
install COPYING $RPM_BUILD_ROOT%{_datadir}/mserver
install ChangeLog $RPM_BUILD_ROOT%{_datadir}/mserver

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mserver
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/mserver
touch $RPM_BUILD_ROOT%{_sysconfdir}/mserver.conf

mv mchat/README README.mchat
rm -rf {docs/images,isdn,firewallscripts/{ipfwadm,ipchain}scripts}/CVS

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	docs/index.html README AUTHORS ChangeLog README.mchat mserver/PROTOCOL \
	mserver/mserver.conf isdn/{ipppd*,isdn.txt} \
	firewallscripts/{ipfwadm,ipchain}scripts/client{up,down}

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add mserver
if [ -f /var/lock/subsys/mserver ]; then
	/etc/rc.d/init.d/mserver restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mserver start\" to start masqdialer daemon."
fi

%preun
if [ "$1" = 0 ]; then
	if [ -f /var/lock/subsys/mserver ]; then
		/etc/rc.d/init.d/mserver stop >&2
	fi
	/sbin/chkconfig --del mserver
fi

%files
%defattr(644,root,root,755)
%doc *.gz mserver/*.gz docs/*.gz docs/images
%doc firewallscripts/ipfwadmscripts firewallscripts/ipchainscripts isdn
%attr(640,root,root) %{_sysconfdir}/pam.d/mserver
%attr(754,root,root) /etc/rc.d/init.d/mserver
%attr(755,root,root) %{_sbindir}/mserver
%attr(755,root,root) %{_sbindir}/mchat
%attr(755,root,root) %{_sbindir}/authgen
%attr(755,root,root) %{_sbindir}/findstat
%attr(755,root,root) %{_sbindir}/checkstat
%attr(755,root,root) %{_sbindir}/fakelink
%attr(755,root,root) %{_sbindir}/linkdown
%attr(755,root,root) %{_sbindir}/linkup
%{_datadir}/mserver/COPYING
%{_datadir}/mserver/ChangeLog
%{_mandir}/man*/*
%config(noreplace) %ghost %{_sysconfdir}/mserver.conf
