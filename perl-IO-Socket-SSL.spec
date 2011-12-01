#
# Rebuild switch:
#  --with sessiontests		enable session tests
#

Name:		perl-IO-Socket-SSL
Version:	1.31
Release:	2%{?dist}
Summary:	Perl library for transparent SSL
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/IO-Socket-SSL/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Test::Simple)
BuildRequires:	perl(IO::Socket::INET6), perl(Net::LibIDN), perl(Net::SSLeay) >= 1.21
BuildRequires:	procps
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(Net::LibIDN)

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}
for f in README SSL.pm; do
	/usr/bin/iconv -f iso-8859-1 -t utf-8 -o $f{.utf8,}; %{__mv} $f{.utf8,}
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%check
# Avoid running the session tests (spawns servers, requires 3 free ports
# and possibly manual configuration).
%{?!_with_sessiontests:%{__mv} t/sessions.t t/sessions.t.disable}
%{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc BUGS Changes README docs/ certs/ example/ util/
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Socket::SSL.3pm*

%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.31-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31 (see Changes for details)

* Thu Aug 20 2009 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30 (fix memleak when SSL handshake failed)
- Add buildreq procps needed for memleak test

* Mon Jul 27 2009 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - various regex fixes for i18n and service names
  - fix warnings from perl -w (CPAN RT#48131)
  - improve handling of errors from Net::ssl_write_all

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul  4 2009 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26 (verify_hostname_of_cert matched only the prefix for the
  hostname when no wildcard was given, e.g. www.example.org matched against a
  certificate with name www.exam in it [#509819])

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25 (fix t/nonblock.t for OS X 10.5 - CPAN RT#47240)

* Thu Apr  2 2009 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24 (add verify hostname scheme ftp, same as http)

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23 (complain when no certificates are provided)

* Sat Jan 24 2009 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to latest upstream version: 1.22

* Thu Jan 22 2009 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to latest upstream version: 1.20

* Tue Nov 18 2008 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to latest upstream version: 1.18
- BR: perl(IO::Socket::INET6) for extra test coverage

* Mon Oct 13 2008 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to latest upstream version: 1.17

* Mon Sep 22 2008 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to latest upstream version: 1.16

* Sat Aug 30 2008 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to latest upstream version: 1.15
- Add buildreq and req for perl(Net::LibIDN) to avoid croaking when trying to
  verify an international name against a certificate

* Wed Jul 16 2008 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to latest upstream version: 1.14
- BuildRequire perl(Net::SSLeay) >= 1.21

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-4
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-3
- Rebuild for new perl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.12-2
- Cosmetic spec changes suiting new maintainer's preferences

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.12-1
- Update to latest upstream version: 1.12
- Fix license tag
- Add BuildRequires for ExtUtils::MakeMaker and Test::Simple
- Fix package review issues:
- Source URL
- Resolves: bz#226264

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.02-1
- Upgrade to latest CPAN version: 1.02

* Mon Sep 18 2006 Warren Togami <wtogami@redhat.com> - 1.01-1
- 1.01 bug fixes (#206782)

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> - 0.998-1
- 0.998 with more important fixes

* Tue Aug 01 2006 Warren Togami <wtogami@redhat.com> - 0.994-1
- 0.994 important bugfixes (#200860)

* Tue Jul 18 2006 Warren Togami <wtogami@redhat.com> - 0.991-1
- 0.991

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.97-3
- Import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-2
- Rebuild for FC5 (perl 5.8.8).
- Rebuild switch: "--with sessiontests".

* Mon Jul 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.97-1
- 0.97.
- Convert docs to UTF-8, drop some unuseful ones.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.96-4
- Rebuilt

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-3
- Disable session test suite even if Net::SSLeay >= 1.26 is available.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.2
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sat May  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- Update to 0.96.
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.95-0.fdr.1
- First build.
