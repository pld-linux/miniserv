Summary:	Tool to execute charge of Internet subscribtion
Summary(pl.UTF-8):	Narzędzie do egzekwowania opłat abonamentowych za Internet
Name:		miniserv
Version:	01
Release:	2
License:	GPL
Group:		Networking/Utilities
Source0:	%{name}.tgz
# Source0-md5:	f7aebb2d54edb3f043f4a8fc476169bf
Source1:	%{name}.inetd
Source2:	%{name}.txt
Source3:	%{name}-PLD.txt
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-off.patch
Patch2:		%{name}-gcc33.patch
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_miniservdir /home/services/%{name}

%description
This tool is for execute charge of Internet subscribtion. You do only
a redirection at firewall and person, who don't pay for internet get
nice page (you can create own page).

%description -l pl.UTF-8
Narzędzie służy do egzekwowania opłat abonamentowych za Internet.
Odpowiednie przekierowanie na firewallu i już osobie, która nie płaci
nam - wyświetla się piękny komunikat (który możemy sobie zdefiniować).

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__cc} %{rpmcflags} -Wall miniserv.c -o miniserv

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_miniservdir},%{_sysconfdir}/sysconfig/rc-inetd}

install miniserv	$RPM_BUILD_ROOT%{_sbindir}
install off/off.html	$RPM_BUILD_ROOT%{_miniservdir}
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/miniserv
install %{SOURCE2}	./
install %{SOURCE3}	./

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc miniserv.txt miniserv-PLD.txt
%attr(755,root,root) %{_sbindir}/miniserv
%{_miniservdir}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/miniserv
