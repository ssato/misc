# .. seealso:: https://fedoraproject.org/wiki/Packaging:Python
%global pkgname jieba 
%global desctxt \
Jieba, Chinese for "to stutter" is a Chinese text segmentation module to support \
three types of segmentation mode, \
- Accurate Mode attempts to cut the sentence into the most accurate \
  segmentations, which is suitable for text analysis. \
- Full Mode gets all the possible words from the sentence. Fast but not accurate. \
- Search Engine Mode, based on the Accurate Mode, attempts to cut long words \
  into several short words, which can raise the recall rate. Suitable for \
  search engines. \
supports Traditional Chinese and customized dictionaries.

Name:           python-%{pkgname}
Version:        0.39
Release:        1%{?dist}
Summary:        Python Chinese word segmentation module
License:        MIT
URL:            https://github.com/fxsjy/jieba
Source0:        %{pkgname}-%{version}.zip
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description    %{desctxt}

%package        -n python2-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkgname}}

%description    -n python2-%{pkgname} %{desctxt}

%if %{with python3}
%package        -n python3-%{pkgname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkgname}}

%description    -n python3-%{pkgname} %{desctxt}
%endif

%prep
%autosetup -n %{pkgname}-%{version}

cat << EOF > README.Fedora
%{desctxt}

See also:

- github: https://github.com/fxsjy/jieba
EOF

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
%doc README.Fedora
%if 0%{?rhel} == 7
%{python_sitelib}/*
%else
%{python2_sitelib}/*
%endif

%if %{with python3}
%files          -n python3-%{pkgname}
%doc README.Fedora
%{python3_sitelib}/*
%endif

%changelog
* Sun Oct 21 2018 Satoru SATOH <ssato@redhat.com> - 0.39-1
- Initial packaging
