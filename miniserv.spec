Summary:	miniserv
Summary(pl):	Narzêdzie do egzekwowania op³at abonamentowych
Name:		miniserv
Version:	01
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	%{name}.tgz
Source1:	%{name}.inetd
Patch0:		%{name}-PLD.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%define		_miniservdir /home/services/httpd/%{name}/

%description

%description -l pl

%prep
%setup -q -n %{name}
%patch -p1

%build
%{__cc} %{rpmcflags} -Wall miniserv.c -o miniserv

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_miniservdir},%{_sysconfdir}/sysconfig/rc-inetd/}

install miniserv	$RPM_BUILD_ROOT%{_sbindir}
install off/off.html	$RPM_BUILD_ROOT%{_miniservdir}
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/miniserv

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi
 
%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/miniserv
%{_miniservdir}/
%{_sysconfdir}/sysconfig/rc-inetd/
