## git=c03ab92
%global git     c03ab92
%global uuid    system-monitor@paradoxxx.zero.gmail.com
%global github  paradoxxxzero-gnome-shell-system-monitor-applet

Name:           gnome-shell-system-monitor-applet
Version:        1.92.0
Release:        1.git%{git}%{?dist}
Summary:        A gnome-shell extension to monitor system resources
Group:          User Interface/Desktops
License:        GPLv3+
URL:            https://github.com/paradoxxxzero/gnome-shell-system-monitor-applet
#Source0:        https://github.com/paradoxxxzero/gnome-shell-system-monitor-applet/tarball/master/%{github}-%{git}.tar.gz
Source0:        https://github.com/paradoxxxzero/gnome-shell-system-monitor-applet/tarball/master/%{name}-%{git}.tar.gz
BuildArch:      noarch
Requires:       gnome-shell >= 3.0.1
BuildRequires:  intltool
BuildRequires:  glib2-devel


%description
Gnome shell system monitor extension is a gnome-shell extension that adds
monitors on the top bar to show various system resource statistics.


%prep
%setup -q -n %{github}-%{git}


%build
# Nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}
install -Dp -m 0644 %{uuid}/{extension.js,metadata.json,stylesheet.css} \
  %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/

mkdir -p %{buildroot}%{_bindir}
install -m 755 system-monitor-applet-config.py \
  %{buildroot}%{_bindir}/system-monitor-applet-config

mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 system-monitor-applet-config.desktop \
  %{buildroot}%{_datadir}/applications/

# something is broken in message catalogs. Disables it for a while:
#for lng in cs_CZ es_MX fa zh_CN; do \
#  mkdir -p %{buildroot}%{_datadir}/locale/LC_MESSAGES/$lng; \
#  msgfmt po/$lng/system-monitor-applet.po -o \
#        %{buildroot}%{_datadir}/locale/LC_MESSAGES/$lng/system-monitor-applet.mo; \
#done

mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas
install -m 644 org.gnome.shell.extensions.system-monitor.gschema.xml \
  %{buildroot}%{_datadir}/glib-2.0/schemas


%posttrans
glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas || :


%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/*
%{_datadir}/gnome-shell/extensions/%{uuid}
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/*
#%{_datadir}/locale/LC_MESSAGES/*/system-monitor-applet.mo


%changelog
* Wed Jun 22 2011 Satoru SATOH <ssato@redhat.com> - 1.92.0-1.gitc03ab92
- Initial package
