%define tname   faenza

Name:           %{tname}-icon-theme
Summary:        Faenza icon theme
Version:        1.3
Release:        1%{?dist}
BuildArch:      noarch
License:        GPLv3
Group:          User Interface/Desktops
URL:            http://code.google.com/p/faenza-icon-theme/
Source0:        %{name}_%{version}.zip

%description
This icon theme for Gnome provides monochromatic icons for panels, toolbars and
buttons and colourful squared icons for devices, applications, folder, files
and Gnome menu items. Four themes are included to fit with light or dark
themes/panels.

%prep
%setup -qc

%build
for f in *.tar.gz; do tar xf $f; done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/{icons,themes}
for d in Faenza-Ambiance Faenza-Dark Faenza-Darker Faenza-Darkest Faenza-Radiance Faenza; do
    cp -a $d $RPM_BUILD_ROOT%{_datadir}/icons
done
for d in Faenza Faenza-Dark Faenza-Darkest; do
    cp -a emesene/themes/$d $RPM_BUILD_ROOT%{_datadir}/themes
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog README
%{_datadir}/icons/*
%{_datadir}/themes/*

%changelog
* Thu Jan  9 2014 Satoru SATOH <ssato@redhat.com> - 1.3-1
- Initial packaging
