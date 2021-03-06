Name:           evas_generic_loaders
Version:        1.9.0
Release:        1%{?dist}
Summary:        Extra loaders for GPL loaders and unstable libraries
License:        GPLv2+
URL:            http://www.enlightenment.org
Source0:        http://download.enlightenment.org/rel/libs/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  LibRaw-devel 
#BuildRequires:  eina-devel
BuildRequires:  efl-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  librsvg2-devel 
BuildRequires:  libspectre-devel
BuildRequires:  libspectre-devel
BuildRequires:  poppler-devel
BuildRequires:  zlib-devel

%Description
These are additional "generic" loaders for Evas that are stand-alone
executables that evas may run from its generic loader module. This
means that if they crash, the application loading the image does not
crash also. In addition the licensing of these binaries will not
affect the license of any application that uses Evas as this uses a
completely generic execution system that allows anything to be plugged
in as a loader.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

%files
%doc AUTHORS COPYING README
%{_libdir}/evas/utils


%changelog
* Fri Mar 21 2014 - Satoru SATOH <satoru.satoh@gmail.com> - 1.9.0-1
- New upstream
- Fix the rpm name; s/_/-/g
- Switched a build dependency to efl-devel successor of eina-devel instead of eina-devel

* Fri Jan 24 2014 - Satoru SATOH <satoru.satoh@gmail.com> - 1.8.1-1
- New upstream

* Mon Aug 19 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Initial Build
