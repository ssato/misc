Name:           evas_generic_loaders
Version:        1.8.1
Release:        1%{?dist}
Summary:        Extra loaders for GPL loaders and unstable libraries
License:        GPLv2+
URL:            http://www.enlightenment.org
Source0:        http://download.enlightenment.org/rel/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  libeina-devel
BuildRequires:  gstreamer-devel 
BuildRequires:  poppler-devel 
BuildRequires:  LibRaw-devel 
BuildRequires:  librsvg2-devel 
BuildRequires:  libspectre-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  libspectre-devel

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
%configure --disable-static
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

%files
%doc AUTHORS COPYING README
%{_libdir}/evas/utils


%changelog
* Fri Jan 24 2014 - Satoru SATOH <satoru.satoh@gmail.com> - 1.8.1-1
- New upstream

* Mon Aug 19 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Initial Build
