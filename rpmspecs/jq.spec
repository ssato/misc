Name:           jq
Version:        1.3
Release:        1%{?dist}
Summary:        A lightweight and flexible command-line JSON processor
Group:          Applications/Text
License:        MIT
URL:            http://stedolan.github.io/jq/
Source0:        http://stedolan.github.io/jq/download/source/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  flex
BuildRequires:  bison


%description
jq is like sed for JSON data – you can use it to slice and filter and map and
transform structured data with the same ease that sed, awk, grep and friends
let you play with text.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# These are included automatically and do not need to be installed.
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/jq/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README AUTHORS
%{_bindir}/jq
%{_mandir}/man1/jq.1.gz


%changelog
* Fri Jul 12 2013 Satoru SATOH <ssato@redhat.com> - 1.3-1
- Initial packaging
