Name:           conky_colors
Version:        0.0.1
Release:        1.git.fa637f57eb%{?dist}   
Summary:        An easier way to configure Conky 
License:        GPLv3+
URL:            https://github.com/helmuthdu/conky_colors
#Source0:        https://github.com/helmuthdu/conky_colors/archive/master.zip
Source0:        %{name}-master.zip
Patch1:         conky_colors-master-Makefile-destdir.patch
#BuildRequires:  gmp-devel
Requires:  conky

%description
Conky_colors is an easier way to configure Conky.

%prep
%setup -q -n %{name}-master
%patch1 -p1 -b .destdir

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc AUTHORS ChangeLog README.md
%{_bindir}/*
%{_datadir}/conkycolors/*/*
%{_datadir}/fonts/*.*

%changelog
* Thu Nov 27 2014 Satoru SATOH <ssato@redhat.com> - 0.0.1-1.git.fa637f57eb
- Initial packaging.
