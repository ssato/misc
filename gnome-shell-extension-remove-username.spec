%global         pkgid removeusername@fpmurphy.com


Name:           gnome-shell-extension-remove-username
Version:        2.0
Release:        1%{?dist}
Summary:        A gnome-shell extension for removing the username on top panel status menu

Group:          User Interface/Desktops
License:        GPLv2
URL:            http://www.fpmurphy.com/gnome-shell-extensions/
Source0:        http://www.fpmurphy.com/gnome-shell-extensions/removeusername-%{version}.tar.gz
BuildArch:      noarch
Requires:       gnome-shell >= 3.2.1


%description
Remove the username displayed on top panel status menu.


%prep
%setup -q -n %{pkgid}


%build
# Nothing to build


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/gnome-shell/extensions/%{pkgid}
for f in extension.js metadata.json
do
        install -m 0644 $f $RPM_BUILD_ROOT%{_datadir}/gnome-shell/extensions/%{pkgid}/
done


%files
%defattr(-,root,root,-)
%doc README
%{_datadir}/gnome-shell/extensions/%{pkgid}/


%changelog
* Tue Jan  3 2012 Satoru SATOH <satoru.satoh@gmail.com> - 2.0-1
- Initial package
