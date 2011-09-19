%define  savedir  /var/lib/pmaker/preserved
%define  newdir  /var/lib/pmaker/installed

Name:           texlive-data-ja
Version:        0.0.1
Release:        1%{?dist}
Summary:        Site (ja) local configuraiton for texlive
Group:          Applications/Publishing
License:        MIT
URL:            http://github.com/ssato/misc/texlive-data-ja
Source0:        %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       ipa-ex-mincho-fonts, ipa-ex-gothic-fonts, sazanami-mincho-fonts, sazanami-gothic-fonts, xdvik, dvipdfmx, texlive-east-asian, poppler-data


%description
This package provides some backup data collected on
localhost.localdomain by Satoru SATOH at Mon, 19 Sep 2011 09:23:19 +0000.


%package        overrides
Summary:        Some more extra data override files owned by other packages
Group:          Applications/Publishing
Requires:       %{name} = %{version}-%{release}
Requires:       texlive-texmf = 0:2007-36.fc14


%description    overrides
Some more extra data will override and replace other packages'.


%prep
%setup -q


%build
%configure --quiet --enable-silent-rules
make %{?_smp_mflags} V=0


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/var/lib/texlive-data-ja-overrides/saved
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides
install -m 755 apply-overrides $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides
install -m 755 revert-overrides $RPM_BUILD_ROOT%{_libexecdir}/%{name}-overrides


%clean
rm -rf $RPM_BUILD_ROOT

%post           overrides
if [ $1 = 1 -o $1 = 2 ]; then    # install or update
    %{_libexecdir}/%{name}-overrides/apply-overrides
fi


%preun          overrides
if [ $1 = 0 ]; then    # uninstall (! update)
    %{_libexecdir}/%{name}-overrides/revert-overrides
fi


%files
%defattr(-,root,root,-)
%doc README
%doc MANIFEST
/etc/fonts/conf.d/90-texlive-local.conf
%attr(0755, -, -) /usr/bin/tex2pdf


%files          overrides
%defattr(-,root,root,-)
%doc MANIFEST.overrides
%dir /var/lib/texlive-data-ja-overrides/saved
%{_libexecdir}/%{name}-overrides/*-overrides
/var/lib/texlive-data-ja-overrides/new/usr/share/texmf/web2c/texmf.cnf


%changelog
* Mon Sep 19 2011 Satoru SATOH <satoru.satoh@gmail.com> - 2007-36.fc14
- Initial packaging.
