%if 0%{?fedora}
%global with_python3 0%{!?_without_python3:1}
%endif

%global pkgname normality

%define _summary Text normalization library for python
%define _desc \
Normality is a Python micro-package that contains a small set of text \
normalization functions for easier re-use. These functions accept a snippet of \
unicode or utf-8 encoded text and remove various classes of characters, such as \
diacritics, punctuation etc. This is useful as a preparation to further text \
analysis.

Name:           python-%{pkgname}
Version:        0.3.9
Release:        1%{?dist}
Summary:        %{_summary}
Group:          Development/Languages
License:        MIT
URL:            https://github.com/pudo/dataset
# From https://pypi.python.org/pypi/%{pkgname}
Source0:        %{pkgname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools

%description
%{_desc}

%package -n     python2-%{pkgname}
Summary:        %{_summary}
Requires:       python2-setuptools
Requires:       python-six
Requires:       python-chardet
%{?python_provide:%python_provide python2-normality}

%description -n python2-%{pkgname}
%{_desc}

%package -n     python3-%{pkgname}
Summary:        %{_summary}
Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-chardet
%{?python_provide:%python_provide python3-normality}

%description -n python3-%{pkgname}
%{_desc}

%prep
%setup -qn %{pkgname}-%{version}

%build
%py3_build
%py2_build
# from https://github.com/pudo/normality
cat << 'EOF' > README.md
# normality

Normality is a Python micro-package that contains a small set of text
normalization functions for easier re-use. These functions accept a
snippet of unicode or utf-8 encoded text and remove various classes
of characters, such as diacritics, punctuation etc. This is useful as
a preparation to further text analysis.

## Example

```python
# coding: utf-8
from normality import normalize, slugify

text = normalize('Nie wieder "Grüne Süppchen" kochen!')
assert text == 'nie wieder grune suppchen kochen'

slug = slugify('My first blog post!')
assert slug == 'my-first-blog-post'
```

## Extended usage

Read the source code, it's twenty lines of stuff.

![RTSL](http://cdn.meme.am/instances/500x/58064648.jpg)

## License

``normality`` is open source, licensed under a standard MIT license.
EOF

%install
%py3_install
%py2_install

%check
#python2 test.py
#python3 test.py

%files -n       python2-%{pkgname}
%doc README.md
%{python2_sitelib}/*

%files -n       python3-%{pkgname}
%doc README.md
%{python3_sitelib}/*

%changelog
* Wed Jan 11 2017 Satoru SATOH <ssato@redhat.com> 0.7.1-1
- Initial RPM release.
