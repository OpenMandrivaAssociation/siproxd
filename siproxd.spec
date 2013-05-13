Summary:	A SIP masquerading proxy with RTP support
Name:		siproxd
Version:	0.7.2
Release:	%mkrel 2
License:	GPLv2+
Group:		System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://siproxd.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/siproxd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	pkgconfig(libosip2) >= 3.0.3
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	docbook-utils
BuildRequires:	docbook-utils-pdf
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

%build
%configure2_5x

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_var}/run/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# fix config
install -m0644 doc/siproxd.conf.example %{buildroot}%{_sysconfdir}/siproxd.conf
install -m0644 doc/siproxd_passwd.cfg %{buildroot}%{_sysconfdir}/siproxd_passwd.cfg
perl -pi -e "s|^user =.*|user = %{name}|g" %{buildroot}%{_sysconfdir}/siproxd.conf

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/false

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
%doc doc/sample_cfg_x-lite.txt doc/siproxd_guide.sgml
%doc doc/html/*.html doc/pdf/*.pdf
%{_initrddir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0640,root,root) %{_sysconfdir}/%{name}.conf.example
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}_passwd.cfg
%{_sbindir}/%{name}
%{_libdir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%dir %{_var}/run/%{name}



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.2-2mdv2011.0
+ Revision: 614891
- the mass rebuild of 2010.1 packages

* Mon Feb 22 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.7.2-1mdv2010.1
+ Revision: 509329
- Update to 0.7.2

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 0.7.1-3mdv2010.0
+ Revision: 445128
- rebuild

* Thu Mar 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.7.1-2mdv2009.1
+ Revision: 358006
- rebuild for latest libosip

* Fri Jul 25 2008 Funda Wang <fwang@mandriva.org> 0.7.1-1mdv2009.0
+ Revision: 249717
- New version 0.7.1
- drop patch0,1, merged upstream

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Thu May 29 2008 Funda Wang <fwang@mandriva.org> 0.7.0-2mdv2009.0
+ Revision: 212864
- add debian patch to make it build

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Thu Jan 24 2008 Colin Guthrie <cguthrie@mandriva.org> 0.7.0-1mdv2008.1
+ Revision: 157699
- Fix docs
- Undo BuildRequire "fix" that was incorrect.
- Fix build requires (libosip2-devel not libosip-devel)
- Update to 0.7.0 (for libosip2-3.x)
- Fix docs sgml
- Add correct docbook dtd for docs
- Remove obsolete no-docs patch
- Remove old prebuilt docs

  + Thierry Vignaud <tv@mandriva.org>
    - fix libosip-devel BR
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 10 2007 Colin Guthrie <cguthrie@mandriva.org> 0.6.0-1mdv2008.1
+ Revision: 116922
- New upstream version.


* Mon Dec 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5.13-2mdv2007.0
+ Revision: 94743
- Import siproxd

* Mon Dec 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5.13-2
- bunzip sources and patches

* Mon Jun 26 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5.13-1mdk
- 0.5.13

* Tue Apr 18 2006 Oden Eriksson <oeriksson@mandriva.com> 0.5.12-1mdk
- 0.5.12 (Major bugfixes)

* Sat May 07 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.11-1mdk
- 0.5.11 final (Major feature enhancements)
- disable html and pdf doc generation as it won't build (P0), 
  provided from their web page for now

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.11-0.2mdk
- run it as the added uid, duh!
- use the %%mkrel macro

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.11-0.1mdk
- 0.5.11

* Fri Dec 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.9-1mdk
- 0.5.9

* Sun Aug 29 2004 Franck Villaume <fvill@freesurf.fr> 0.5.7-1mdk
- 0.5.7
- move to libosip2

