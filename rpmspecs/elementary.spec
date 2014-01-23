Name:           elementary
Version:        1.8.3
Release:        1%{?dist}
Summary:        Basic widget set that is easy to use based on EFL
License:        LGPLv2+
URL:            http://www.enlightenment.org
Source0:        http://download.enlightenment.org/rel/libs/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  efl-devel
BuildRequires:  efl
#BuildRequires:  evas-generic-loaders
BuildRequires:  gettext

%description
Elementary is a widget set. It is a new-style of widget set much more canvas
object based than anything else.

%package devel
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Stuff

%description devel
Devel packages

%prep
%setup -q

%build
%configure --disable-rpath --disable-doc --disable-static --disable-elementary-test
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name 'elementary_testql.so' -delete
find %{buildroot} -name 'elementary_test.desktop' -delete
find %{buildroot} -name 'elementary_testql' -delete


desktop-file-install                                                                    \
        --delete-original                                                               \
        --dir=%{buildroot}%{_datadir}/applications                                      \
%{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/*
%{_libdir}/libelementary.so.1*
%{_datadir}/applications/elementary_config.desktop
%{_datadir}/elementary
%{_datadir}/icons/elementary.png
%{_libdir}/edje/modules/elm
%{_libdir}/elementary

%files devel
%{_includedir}/elementary-1
%{_libdir}/libelementary.so
%{_libdir}/pkgconfig/elementary.pc
%{_libdir}/cmake/Elementary/*.cmake

%changelog
* Fri Jan 24 2014 Satoru SATOH <satoru.satoh@gmail.com> - 1.8.3-1
- Update to 1.8.3

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.9-1
- Update to 1.7.9

* Mon Oct 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-5
- Add ethumb support and others.

* Fri Sep 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-4
- Fix licensing
- Add icon scriptlets
- Remove elementary_test desktop and binary files
- Fix directory ownership
- Fix unused direct shlib dependency

* Thu Sep 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-3
- Fix build errors

* Tue Sep 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-2
- Remove useless shared object.

* Fri Sep 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8
- Pretty up spec file.

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> 1.7.4-1
- Initial spec
