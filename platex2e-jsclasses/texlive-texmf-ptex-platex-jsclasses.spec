## Where should they go?
%define platexstydir    /usr/share/texmf/ptex/platex/jsclasses
%define tfmfontdir      /usr/share/texmf/fonts/tfm/jis

Name:           texlive-texmf-ptex-platex-jsclasses
Version:        110510
Release:        1%{?dist}
Summary:        Japanese docuemnt style classes for pLaTeX2e
Group:          Applications/Publishing
License:        BSD
URL:            http://oku.edu.mie-u.ac.jp/~okumura/jsclasses
Source0:        http://oku.edu.mie-u.ac.jp/~okumura/jsclasses/jsclasses.zip
Source1:        http://oku.edu.mie-u.ac.jp/~okumura/texfaq/jis-tfm.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       texlive-east-asian


%description
Japanese docuemnt style and class files for pLaTeX2e developed and distributed
under modified BSD license by Haruhiko OKUMURA, famous Japanese LaTeX book
author.


%prep
%setup -q -c -n jsclasses
cat << EOF > README.Fedora

## This is an English translation of part of 'What's this' section in the %URL:
This is the LaTeX2e document class files used in the Japanese books titled
"LaTeX2e Bibunsho-Sakusei-Nyumon". This include the following style files:

* jsarticle corresponding to the style file, jarticle
* jsbook, corresponding to the style file, jbook
* misc styles including okumacro.sty, okuverb.sty and morisawa.sty

Some parameters are tuned to meet the tradition of Japanese composition.

Optional font sizes are 9pt, 10pt, 11pt, 12pt, 14pt, 17pt, 21pt, 25pt, 30pt,
36pt, and 43pt. Larger sized fonts will be fit for presentation slides.

In addition, numerous improvements have been made compared to the original
jarticle/jbook styles. For more detailed information, please take a look at
jsclasses.dtx in the source distribution.

This package is distributed under the modified BSD License as same as pTeX
distributed by ASCII Media Works.
EOF

mkdir jis-tfm && cd jis-tfm && unzip %{SOURCE1}


%build
# nothing to do. .sty files looks included in the source distribution.


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{platexstydir}
for f in *.{cls,sty}; do install -m 644 $f $RPM_BUILD_ROOT%{platexstydir}; done

install -d $RPM_BUILD_ROOT%{tfmfontdir}
for f in jis-tfm/*.tfm; do install -m 644 $f $RPM_BUILD_ROOT%{tfmfontdir}; done


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ ! -x /usr/bin/texhash ]; then
    cat /usr/share/texmf/default.ls-R > /usr/share/texmf/ls-R
    cat /var/lib/texmf/default.ls-R  > /var/lib/texmf/ls-R
else
    [ -x /usr/bin/texconfig-sys ] && /usr/bin/texconfig-sys rehash 2> /dev/null
fi
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
    [ -x /sbin/restorecon ] && /sbin/restorecon -R /var/lib/texmf/
fi


%postun
[ -x /usr/bin/texconfig-sys ] && /usr/bin/texconfig-sys rehash 2> /dev/null && \
[ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled && \
[ -x /sbin/restorecon ] && /sbin/restorecon -R /var/lib/texmf/ || :


%files
%defattr(-,root,root,-)
%doc README.Fedora
%{platexstydir}
%{tfmfontdir}


%changelog
* Wed Sep 21 2011 Satoru SATOH <ssato@redhat.com> - 110510-1
- Initial packaging.
