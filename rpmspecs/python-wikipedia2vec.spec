# .. seealso:: https://fedoraproject.org/wiki/Packaging:Python
%global pkgname wikipedia2vec
%global desctxt \
Wikipedia2Vec is a tool used for obtaining embeddings (vector representations) \
of words and entities from Wikipedia. It is developed and maintained by \
Studio Ousia.

Name:           python-%{pkgname}
Version:        0.2.7
Release:        1%{?dist}
Summary:        A tool for learning vector representations of words and entities from Wikipedia
License:        ASL 2.0
URL:            https://wikipedia2vec.github.io/wikipedia2vec/
Source0:        %{pkgname}-%{version}.tar.gz

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-Cython
BuildRequires:  python2-numpy
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython
BuildRequires:  python3-numpy
%endif

%description    %{desctxt}

%package        -n python2-%{pkgname}
Summary:        %{summary}
Requires:       python2-click
Requires:       python2-jieba
Requires:       python2-joblib
Requires:       python2-marisa-trie
Requires:       python2-mwparserfromhell
Requires:       python2-numpy
Requires:       python2-scipy
Requires:       python2-six
Requires:       python2-tqdm
%{?python_provide:%python_provide python2-%{pkgname}}

%description    -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package        -n python3-%{pkgname}
Summary:        %{summary}
Requires:       python3-click
Requires:       python3-jieba
Requires:       python3-joblib
Requires:       python3-marisa-trie
Requires:       python3-mwparserfromhell
Requires:       python3-numpy
Requires:       python3-scipy
Requires:       python3-six
Requires:       python3-tqdm
%{?python_provide:%python_provide python3-%{pkgname}}

%description    -n python3-%{pkgname} %{desctxt}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files          -n python2-%{pkgname}
%doc README.md
%if 0%{?rhel} == 7
%{python_sitearch}/*
%else
%{python2_sitearch}/*
%endif

%if %{with python3}
%files          -n python3-%{pkgname}
%doc README.md
%{python3_sitearch}/*
%endif
%{_bindir}/*

%changelog
* Mon Oct 22 2018 Satoru SATOH <ssato@redhat.com> - 0.2.7-1
- Initial packaging
