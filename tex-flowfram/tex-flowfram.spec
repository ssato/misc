%define orgname flowfram

## Where should they go?
%define latexstydir     /usr/share/texmf/tex/latex
%define platexstydir    /usr/share/texmf/ptex/platex/base

Name:           tex-%{orgname}
Version:        1.13
Release:        1%{?dist}
Summary:        Tex style to create frames for posters, brochures or magazines
Group:          Applications/Publishing
License:        LPPL
URL:            http://www.ctan.org/tex-archive/macros/latex/contrib/%{orgname}
Source0:        http://mirror.ctan.org/macros/latex/contrib/%{orgname}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  texlive-latex
BuildRequires:  texlive-east-asian
Requires:       texlive-texmf-latex


%description
This package is designed to enable you to create frames in a document such that
the contents of the document environment flow from one frame to the next in the
order in which they were defined.  This is useful for creating posters or
magazines or any other form of document that does not conform to the standard
one or two column layout.


%package        platex
Summary:        %{orgname} style package for platex
Group:          Applications/Publishing
Requires:       %{name} = %{version}-%{release}
Requires:       texlive-east-asian


%description    platex
This package provides style file compiled for platex.


%prep
%setup -q


%build
latex flowfram.ins && mv flowfram.sty flowfram.latex.sty
platex flowfram.ins && mv flowfram.sty flowfram.platex.sty


%install
rm -rf $RPM_BUILD_ROOT

install -d %{latexstydir}/%{orgname}
install -m 644 flowfram.latex.sty %{latexstydir}/%{orgname}

install -d %{platexstydir}
install -m 644 flowfram.platex.sty %{platexstydir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README CHANGES
%doc flowfram.pdf ffuserguide.pdf ffuserguide.html
%doc brochure.pdf brochure.tex
%doc news.tex news2.tex news.pdf news2.pdf
%doc egg.eps egg.pn poster.tex sheep.png poster.pdf sheep.eps
%{latexstydir}/%{orgname}


%files          platex
%{platexstydir}/*


%changelog
* Mon Sep 19 2011 Satoru SATOH <ssato@redhat.com> - 1.13-1
- Initial packaging.
