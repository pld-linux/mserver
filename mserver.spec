Summary:	Masq Dialer deamon
Name:		mserver
Version:	0.5.5
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Vendor:		Chares P. Wright <cpwright@cpwright.com>
URL:		http://w3.cpwright.com
Source0:	ftp://ftp.cpwright.com/pub/mserver/c-%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.pam
Patch0:		%{name}-config.patch
Patch1:		%{name}-dial.patch
Patch2:		%{name}-Makefile.patch
Prereq:		chkconfig
Prereq:		rc-scripts >= 0.2.1
Requires:	ppp
BuildRequires:	automake
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		%{_sbindir}

%description
The masqdialer system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet access
on a Linux box without having to use telnet. It's based on a
client/server approach so any TCP/IP enabled system should be able to
take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

%description -l pl
Masqdialer pozwala autoryzowanym u�ytkownikom sieci LAN na
manipulowanie interfejsami sieciowymi (zwykle modemem), kt�re daj�
dost�p do Internetu poprzez "pude�ko" z Linuxem bez potrzeby u�ywania
telnetu. Jest on bazowany na architekturze klient/server, wi�c ka�dy
system z aktywnym TCP/IP powinien by� w stanie korzysta�, je�eli tylko
klient zostanie napisany. Aktualnie: Linux, Windows, NetBSD oraz
systemy z implementacj� Javy lub przegl�dark� Web.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,rc.d/init.d} \

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mserver
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/mserver

touch $RPM_BUILD_ROOT%{_sysconfdir}/mserver.conf

mv mchat/README README.mchat
rm -rf {docs/images,isdn,firewallscripts/{ipfwadm,ipchain}scripts}/CVS

gzip -9nf docs/index.html README AUTHORS ChangeLog README.mchat mserver/PROTOCOL \
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
%config(noreplace) %ghost %{_sysconfdir}/mserver.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
