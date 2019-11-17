# Forked from:
# https://apps.fedoraproject.org/packages/python-gensim/sources/

# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# Settings used for build from snapshots.
%{!?rel_build:%global commit            d1c6d58b9acfec97e6c5d677c652293ae2119276}
%{!?rel_build:%global commit_date       20140510}
%{!?rel_build:%global shortcommit       %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global gitver            git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global gitrel            .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global gittar            %{name}-%{version}-%{gitver}.tar.gz}
%{?rel_build: %global gittar            %{name}-%{version}.tar.gz}

%global         common_description                                      \
Gensim is a Python library for topic modelling, document indexing       \
and similarity retrieval with large corpora.  Target audience is        \
the natural language processing (NLP) and information retrieval         \
(IR) community.                                                         \
                                                                        \
Features:                                                               \
                                                                        \
  * All algorithms are memory-independent w.r.t. the corpus size        \
(can process input larger than RAM).                                    \
  * Intuitive interfaces                                                \
    - easy to plug in your own input corpus/datastream (trivial         \
streaming API)                                                          \
    - easy to extend with other Vector Space algorithms (trivial        \
transformation API)                                                     \
  * Efficient implementations of popular algorithms, such as online     \
Latent Semantic Analysis (LSA/LSI), Latent Dirichlet Allocation (LDA),  \
Random Projections (RP), Hierarchical Dirichlet Process (HDP) or        \
word2vec deep learning.                                                 \
  * Distributed computing: can run Latent Semantic Analysis and Latent  \
Dirichlet Allocation on a cluster of computers, and word2vec on         \
multiple cores.                                                         \
  * Extensive HTML documentation and tutorials.

%global                 pypi_name gensim

Name:                   python-%{pypi_name}
Version:                3.8.1
Release:                1%{?dist}
Summary:                Python framework for fast Vector Space Modelling
License:                LGPLv2
URL:                    http://radimrehurek.com/%{pypi_name}/
# Sources for release-builds.
%{?rel_build:Source0:   https://github.com/piskvorky/%{pypi_name}/archive/%{version}.tar.gz#/%{gittar}}
# Sources for snapshot-builds.
%{!?rel_build:Source0:  https://github.com/piskvorky/%{pypi_name}/archive/%{commit}.tar.gz#/%{gittar}}

BuildRequires:          fdupes
BuildRequires:          gcc
BuildRequires:          python3-Cython
BuildRequires:          python3-devel
BuildRequires:          python3-nose
BuildRequires:          python3-numpy
BuildRequires:          python3-scipy
BuildRequires:          python3-setuptools
BuildRequires:          python3-six
BuildRequires:          python3-sphinx
BuildRequires:          python3-sphinxcontrib-programoutput
BuildRequires:          python3-smart_open
BuildRequires:          python3-Pyro4
BuildRequires:          python3-annoy
BuildRequires:          python3-plotly
BuildRequires:          python3-scikit-learn
BuildRequires:          texlive-dvipng
BuildRequires:          texlive-latex
BuildRequires:          texlive-amscls
BuildRequires:          texlive-anyfontsize
BuildRequires:          texlive-ucs

%description %common_description

%package doc
Summary:                Documentation for %{name}
BuildArch:              noarch

%description doc
This package provides the documentation for %{name}.

%package -n python3-%{pypi_name}
Summary:                Python framework for fast Vector Space Modelling
Requires:               python3-numpy
Requires:               python3-scipy
Requires:               python3-six
Requires:               python3-smart_open
Requires:               python3-Pyro4
Requires:               python3-annoy
Requires:               python3-plotly
Requires:               python3-scikit-learn
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %common_description

%package -n python3-%{pypi_name}-test
Summary:                Testsuite for %{name}
Requires:               python3-%{pypi_name}            == %{version}-%{release}
Requires:               python3-nose
%{?python_provide:%python_provide python3-%{pypi_name}-test}

%description -n python3-%{pypi_name}-test
This package provides the testsuite for %{name}.  You don't need it
for everyday usage.


%prep
%setup -q%{?rel_build:n %{pypi_name}-%{version}}%{!?rel_build:n %{pypi_name}-%{commit}}

# Fix EOL-encodings.
_file="docs/src/_static/js/jquery-migrate-1.1.1.min.js" &&              \
sed -i.orig -e 's!\r$!!g' ${_file} &&                                   \
touch -r ${_file}.orig ${_file} && rm -rf ${_file}.orig

# Remove hashbangs
for _file in `find . -type f -name '*.py'`; do
  grep -q python $_file 2>/dev/null >/dev/null && \
  sed -i.new -r '
s/program-output:: python/&3/g
1{\@^#!/usr/bin/env python@d}
' $_file || :
done

%build
%py3_build
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
  %{__python3} %{py_setup} %{?py_setup_args} build_ext

%install
%py3_install
find %{buildroot} -type f -name '*.pyx' -print0 | xargs -0 rm -f
%fdupes %{buildroot}
%_fixperms %{buildroot}/*

# Build the autodocs.  We need the PYTHONPATH for this.
export PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitearch}"
pushd docs/src
sed -i.save -r '
s/sphinxcontrib.napoleon/sphinx.ext.napoleon/
/sys.path.insert/a \
sys.path.insert(0, "%{buildroot}%{python3_sitelib}")\nsys.path.insert(0, "%{buildroot}%{python3_sitearch}")' conf.py
make html
rm -f _build/html/.buildinfo
%fdupes _build/html
popd


%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitearch}"
pushd %{buildroot}%{python3_sitearch}/%{pypi_name}
nosetests-%{python3_version} -v -e testLargeMmap -e testPersistence || :
popd

%files doc
%doc CHANGELOG* COPYING* README*
%doc docs/src/_build/html %{pypi_name}/examples

%files -n python3-%{pypi_name}
%doc CHANGELOG* COPYING* README*
%dir %{python3_sitearch}/%{pypi_name}
%exclude %{python3_sitearch}/%{pypi_name}/nosy.py
%exclude %{python3_sitearch}/%{pypi_name}/__pycache__/nosy*
%exclude %{python3_sitearch}/%{pypi_name}/test
%{python3_sitearch}/%{pypi_name}/*
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%files -n python3-%{pypi_name}-test
%{python3_sitearch}/%{pypi_name}/nosy.py
%{python3_sitearch}/%{pypi_name}/__pycache__/nosy*
%{python3_sitearch}/%{pypi_name}/test


%changelog
* Sat Nov 16 2019 Satoru SATOH <satoru.satoh@gmail.com> - 3.8.1-1
- Forked and cleanup the RPM SPEC
- New upstream
- Rename python3-gensim{-core,} to resolve rhbz#1693064 and rhbz#1770829
- Subpackage python3-gensim-addons has been removed
- Added runtime and build time dependency

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-21
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-20
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Björn Esser <besser82@fedoraproject.org> - 0.10.0-18
- Use %%py3_{build,install} macros

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-16
- Subpackages python2-gensim-core, python2-gensim-addons, python2-gensim-test have been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-14
- Rebuilt for Python 3.7

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-13
- Fix python2 subpackage naming

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-12
- Python 2 binary package renamed to python2-gensim
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 17 2014 Karsten Hopp <karsten@redhat.com> 0.10.0-3
- fix duplicate changlog section, current rpm doesn't accept it

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Björn Esser <bjoern.esser@gmail.com> - 0.10.0-1
- new upstream release (#1100734)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-0.5.git20140510.d1c6d58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.2-0.4.git20140510.d1c6d58
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun May 11 2014 Björn Esser <bjoern.esser@gmail.com> - 0.9.2-0.3.git20140510.d1c6d58
- fix internal dependencies of Python3-pkgs

* Sun May 11 2014 Björn Esser <bjoern.esser@gmail.com> - 0.9.2-0.2.git20140510.d1c6d58
- updated to new snapshot git20140510.d1c6d58b9acfec97e6c5d677c652293ae2119276
- add Python3-build
- minor improvements to spec-file

* Thu May 01 2014 Björn Esser <bjoern.esser@gmail.com> - 0.9.2-0.1.git20140423.e56d7fd
- updated to new snapshot git20140423.e56d7fd1bb643d772030e645442af3961a4b88aa
- dropped Patch0
- python-six is now unbundled in upstream-tarball

* Mon Apr 21 2014 Björn Esser <bjoern.esser@gmail.com> - 0.9.1-1
- initial rpm release (#1089710)
