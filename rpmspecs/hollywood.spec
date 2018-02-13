Name:           hollywood
Version:        1.12
Release:        1%{?dist}
Summary:        fill your console with Hollywood melodrama technobabble
License:        ASL 2.0
URL:            https://github.com/dustinkirkland/hollywood
Source0:        %{url}/archive/master.zip
Requires:       byobu
Requires:       apg
Requires:       bmon
Requires:       ccze
Requires:       htop
Requires:       jp2a
Requires:       mlocate
Requires:       moreutils
Requires:       mplayer
Requires:       openssh-clients
Requires:       nodejs-speedometer
Requires:       tree
Requires:       vim-enhanced
# TODO: Not available or available but different RPM names...
#Requires:       bsdmainutils
#Requires:       cmatrix
BuildArch:      noarch

%description
This utility will split your console into a multiple panes of genuine
technobabble, perfectly suitable for any Hollywood geek melodrama.  It is
particularly suitable on any number of computer consoles in the background of
any excellent schlock technothriller.

%prep
%autosetup -n %{name}-master

%build

%install
install -d %{buildroot}{%{_bindir},%{_libdir},%{_datadir}}
for x in bin/*; do install -m 755 $x %{buildroot}%{_bindir}/; done
for d in hollywood wallstreet; do
    install -d %{buildroot}%{_libdir}/$d
    install -d %{buildroot}%{_datadir}/$d
    for f in lib/$d/*; do install $f %{buildroot}%{_libdir}/$d/; done
    for f in share/$d/*; do install $f %{buildroot}%{_datadir}/$d/; done
done
install -d %{buildroot}%{_datadir}/man/man1
for f in share/man/man1/*; do install $f %{buildroot}%{_mandir}/man1/; done

%files
%doc README TODO
%{_bindir}/*
%{_libdir}/*/*
%{_datadir}/*/*
%{_mandir}/*/*

%changelog
* Tue Feb 13 2018 Satoru SATOH <ssato@redhat.com> - 1.12-1
- Initial packaging.
