Name:           fcrackzip
Version:        1.0
Release:        1%{?dist}
Summary:        A zip password cracker
License:        GPLv2
URL:            http://oldhome.schmorp.de/marc/fcrackzip.html
Source0:        http://oldhome.schmorp.de/marc/data/%{name}-%{version}.tar.gz
#BuildRequires:  
Requires:       unzip


%description
fcrackzip is an open source, fast, portable and featureful zip password
cracker.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/zipinfo  # conflicts with unzip


%files
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Mon Jun  4 2012 Satoru SATOH <satoru.satoh@gmail.com> - 1.0-1
- Initial packaging.
