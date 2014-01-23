Name:           efl
Version:        1.8.4
Release:        1%{?dist}
Summary:        Enlightenment Foundation libraries
License:        LGPLv2.1+ and GPLv2.1+ and BSD
Group:          System Environment/Libraries
Url:            http://enlightenment.org
Source:         http://download.enlightenment.org/rel/%{name}-%{version}.tar.gz
# From efl/README:
BuildRequires:  bullet-devel
BuildRequires:  dbus-devel
BuildRequires:  doxygen 
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  giflib-devel
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  iputils 
BuildRequires:  libblkid-devel
BuildRequires:  libmount-devel
BuildRequires:  libX11-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXau-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXp-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXtst-devel
BuildRequires:  libcurl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libtiff-devel
BuildRequires:  lua-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  openssl-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
# Extras:
BuildRequires:  libdrm-devel
BuildRequires:  SDL-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  ibus-devel
BuildRequires:  gettext, gettext-devel
BuildRequires:  openjpeg-devel
Provides:       ecore = %{version}-%{release}
Provides:       edje = %{version}-%{release}
Provides:       eet = %{version}-%{release}
Provides:       eeze = %{version}-%{release}
Provides:       efreet = %{version}-%{release}
Provides:       eina = %{version}-%{release}
Provides:       eio = %{version}-%{release}
Provides:       embryo = %{version}-%{release}
Provides:       emotion = %{version}-%{release}
Provides:       eo = %{version}-%{release}
Provides:       escape = %{version}-%{release}
Provides:       ethumb = %{version}-%{release}
Provides:       evas = %{version}-%{release}
Obsoletes:      ecore < %{version}-%{release}
Obsoletes:      edje < %{version}-%{release}
Obsoletes:      eet < %{version}-%{release}
Obsoletes:      eeze < %{version}-%{release}
Obsoletes:      efreet < %{version}-%{release}
Obsoletes:      eina < %{version}-%{release}
Obsoletes:      eio < %{version}-%{release}
Obsoletes:      embryo < %{version}-%{release}
Obsoletes:      emotion < %{version}-%{release}
Obsoletes:      eo < %{version}-%{release}
Obsoletes:      escape < %{version}-%{release}
Obsoletes:      ethumb < %{version}-%{release}
Obsoletes:      evas < %{version}-%{release}

%description
Enlightenment Foundation Library

%package        devel
Summary:        Development files for efl
License:        LGPLv2+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files, examples, man and HTML documentation for efl package.

%prep
%setup -q

%build
%configure                            \
            --disable-win32-threads   \
            --disable-notify-win32    \
            --disable-libtool-lock    \
            --disable-static          \
            --enable-ibus

#            --disable-doc             \
make %{?_smp_mflags} V=1

%install
%make_install
#chrpath --delete %{buildroot}%{_libdir}/*/modules/*/*/*/*.so
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
%find_lang %{name}

%post
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%files          -f %{name}.lang
%doc README COPYING NEWS AUTHORS COMPLIANCE
%{_bindir}/*
%{_libdir}/lib*so.*
%{_libdir}/*/*/*/*/module.so
%{_libdir}/*/*/*/*/*/module.so
%{_libdir}/edje/utils/*/epp
%{_libdir}/efreet/*/*
%{_libdir}/ethumb/modules/emotion/*/template.edj
%{_libdir}/ethumb_client/utils/*/ethumbd_slave
%{_libdir}/evas/cserve2/bin/*/*
%{_datadir}/dbus-1/services/org.enlightenment.*.service
%{_datadir}/*/checkme
%{_datadir}/*/include/*.inc
%{_datadir}/eo/gdb/eo_gdb.py*
%{_datadir}/ethumb/frames/default.edj
%{_datadir}/gdb/auto-load/usr/*/*.py*
%{_datadir}/mime/packages/edje.xml

%files          devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/*/*.cmake

%changelog
* Fri Jan 24 2014 Satoru SATOH <satoru.satoh@gmail.com> - 1.8.4-1
- Update to 1.8.4
- Merged all Enlightenment core libraries into EFL

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Tue Sep 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-2
- Fix #1003692

* Sun Aug 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Bump to 1.7.8

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-3
- Disable doc building as it was causing builds to fail

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-2
- Clean up the spec file some more as devel subpackage was not installing.

* Fri Aug 16 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7

* Fri Jun 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6 and clean up spec

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec
