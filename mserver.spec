Summary:	Masq Dialer deamon
Summary(pl):	Serwer MasqDialer - zestawiaj±cy po³±czenia do Internetu
Name:		mserver
Version:	0.5.5
Release:	4
License:	GPL
Vendor:		Chares P. Wright <cpwright@cpwright.com>
Group:		Networking/Daemons
Source0:	http://w3.cpwright.com/mserver/download/c-%{name}-%{version}.tar.gz
# Source0-md5:	ee4348241ac8e42d6b62c93036ffaf71
Source1:	%{name}.init
Source2:	%{name}.pam
Patch0:		%{name}-config.patch
Patch1:		%{name}-dial.patch
Patch2:		%{name}-Makefile.patch
Patch3:		%{name}-errno.patch
URL:		http://w3.cpwright.com/mserver/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pam-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	ppp
Requires:	rc-scripts >= 0.2.1
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
Masqdialer pozwala autoryzowanym u¿ytkownikom sieci LAN na
manipulowanie interfejsami sieciowymi (zwykle modemem), które daj±
dostêp do Internetu poprzez "pude³ko" z Linuksem bez potrzeby u¿ywania
telnetu. Jest on bazowany na architekturze klient/server, wiêc ka¿dy
system z aktywnym TCP/IP powinien byæ w stanie korzystaæ, je¿eli tylko
klient zostanie napisany. Aktualnie: Linux, Windows, NetBSD oraz
systemy z implementacj± Javy lub przegl±dark± Web.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mserver
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/mserver

touch $RPM_BUILD_ROOT%{_sysconfdir}/mserver.conf

mv -f mchat/README README.mchat
rm -rf {docs/images,isdn,firewallscripts/{ipfwadm,ipchain}scripts}/CVS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mserver
if [ -f /var/lock/subsys/mserver ]; then
	/etc/rc.d/init.d/mserver restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mserver start\" to start masqdialer daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mserver ]; then
		/etc/rc.d/init.d/mserver stop >&2
	fi
	/sbin/chkconfig --del mserver
fi

%files
%defattr(644,root,root,755)
%doc docs/index.html README AUTHORS ChangeLog README.mchat mserver/PROTOCOL
%doc mserver/mserver.conf isdn/{ipppd*,isdn.txt}
%doc firewallscripts/ipchainscripts/client{up,down}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime, size,) /etc/pam.d/mserver
%attr(754,root,root) /etc/rc.d/init.d/mserver
%config(noreplace) %ghost %{_sysconfdir}/mserver.conf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
