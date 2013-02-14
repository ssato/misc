# TODO: License check

%define major   1.14i
%define minor   ac20050924p1

Name:           lha
Version:        %{major}_%{minor}
Release:        1%{?dist}
Summary:        LZH file archiver
Group:          Applications/Archiving
License:        Commercial
URL:            http://lha.sourceforge.jp
Source0:        %{name}-%{major}-%{minor}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
LZH file archiver.


%prep
%setup -q -n %{name}-%{major}-%{minor}


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc 00readme.autoconf Hacking_of_LHa
%{_bindir}/*
%{_datadir}/man*/man*/*

%changelog
* Thu Feb 14 2013 Satoru SATOH <satoru.satoh@gmail.com> - 1.14i_ac20050924p1-1
- Initial packaging.
