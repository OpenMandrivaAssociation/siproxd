Summary:	A SIP masquerading proxy with RTP support
Name:		siproxd
Version:	0.7.0
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://siproxd.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/siproxd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		siproxd_guide.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	libosip-devel >= 3.0.3
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	docbook-dtd42-sgml

%description
Siprox is an proxy/masquerading daemon for the SIP protocol.
It handles registrations of SIP clients on a private IP network
and performs rewriting of the SIP message bodies to make SIP
connections possible via an masquerading firewall.
It allows SIP clients (like kphone, linphone) to work behind
an IP masquerading firewall or router.

%prep

%setup -q
%patch0 -p1

%build

%configure

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall

install -d %{buildroot}%{_var}/run/%{name}
install -d %{buildroot}%{_localstatedir}/%{name}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# fix config
install -m0644 doc/siproxd.conf.example %{buildroot}%{_sysconfdir}/siproxd.conf
install -m0644 doc/siproxd_passwd.cfg %{buildroot}%{_sysconfdir}/siproxd_passwd.cfg
perl -pi -e "s|^user =.*|user = %{name}|g" %{buildroot}%{_sysconfdir}/siproxd.conf

%pre
%_pre_useradd %{name} %{_localstatedir}/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog README RELNOTES TODO
%doc doc/FLI4L_HOWTO.txt doc/KNOWN_BUGS doc/RFC3261_compliance.txt doc/sample_cfg_budgetone.txt
%doc doc/sample_cfg_x-lite.txt doc/siproxd_guide.sgml doc/html/*.html
%{_initrddir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0640,root,root) %{_sysconfdir}/%{name}.conf.example
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}_passwd.cfg
%{_sbindir}/%{name}
%dir %{_localstatedir}/%{name}
%dir %{_var}/run/%{name}

