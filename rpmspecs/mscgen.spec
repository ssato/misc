# SEE ALSO: https://bugzilla.redhat.com/show_bug.cgi?id=630754

Name:           mscgen
Version:        0.20
Release:        2%{?dist}
Summary:        Message sequence chart generator
Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.mcternan.me.uk/mscgen
Source0:        http://www.mcternan.me.uk/mscgen/software/%{name}-src-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gd-devel
BuildRequires:  flex
BuildRequires:  bison
Requires:       gd


%description
Mscgen is a small program that parses Message Sequence Chart descriptions and
produces PNG, EPS or server side image maps (ismaps) as the output.  Message
Sequence Charts (MSCs) are a way of representing entities and interactions over
some time period and are often used in combination with SDL. MSCs are popular
in Telecoms to specify how protocols operate although MSCs need not be
complicated to create or use. Mscgen aims to provide a simple text language
that is clear to create, edit and understand, which can also be transformed
into PNG or EPS images.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

# trim <CR> at the tail of each lines;
# (http://fedoraproject.org/wiki/PackageMaintainers/Common_Rpmlint_Issues#wrong-file-end-of-line-encoding)
for f in TODO; do sed -i 's/\r//g' $f; done


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

## Hacks:
# relocate some %doc files installed:
mv examples examples_src && mv $RPM_BUILD_ROOT/%{_datadir}/doc/mscgen/examples ./
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/mscgen
#
# fix the wrong path in the shebung lines:
for f in ./examples/*.msc; do sed -i '1s,/usr/local/bin/mscgen,%{_bindir}/mscgen,' $f; done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README ChangeLog TODO
%doc examples
%{_bindir}/mscgen
%{_mandir}/man1/*


%changelog
* Mon Mar 26 2012 Satoru SATOH <ssato@redhat.com> - 0.20-2
- Changed SOURCE0 for easy build

* Tue Nov 22 2011 Satoru SATOH <ssato@redhat.com> - 0.20-1
- New upstream

* Sun Jan  2 2011 Satoru SATOH <ssato@redhat.com> - 0.18-1
- New upstream

* Sun Jan 11 2009 Satoru SATOH <ssato@redhat.com> - 0.13-1
- New upstream
- Removed sample.msc and install test sources as samples.

* Thu Aug 23 2007 Satoru SATOH <ssato@redhat.com> - 0.8-1
- New upstream

* Thu Aug 23 2007 Satoru SATOH <ssato@redhat.com> - 0.6-1
- Initial packaging.
