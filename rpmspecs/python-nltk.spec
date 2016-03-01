%global mod_name nltk
Name:           python-nltk
Epoch:          1
Version:        3.1
Release:        1%{?dist}
Summary:        Natural Language Toolkit

Group:          Development/Libraries
# The entire source code is ASL 2.0 except nltk/stem/porter.py is
# GPLv2+ with exceptions
License:        ASL 2.0 and GPLv2+ with exceptions
URL:            http://www.nltk.org/
Source0:        http://pypi.python.org/packages/source/n/%{mod_name}/%{mod_name}-%{version}.tar.gz
# https://github.com/nltk/nltk/blob/develop/nltk/sentiment/vader_lexicon.txt
Source10:       vader_lexicon.txt
BuildArch:      noarch

BuildRequires:  python2-devel >= 2.5
BuildRequires:  python-setuptools
Requires:       PyYAML >= 3.09
Requires:       numpy python-matplotlib tkinter

%description
NLTK is a Python package that simplifies the construction of programs
that process natural language; and defines standard interfaces between
the different components of an NLP system.  It was designed primarily
to help teach graduate and undergraduate students about computational
linguistics; but it is also useful as a framework for implementing
research projects.

%package -n python3-%{mod_name}
Summary:        Natural Language Toolkit (Python 3)
BuildRequires:  python3-devel >= 2.5
BuildRequires:  python3-setuptools
Requires:       python3-PyYAML >= 3.09
Requires:       python3-numpy python3-matplotlib python3-tkinter

%description -n python3-%{mod_name}
NLTK is a Python package that simplifies the construction of programs
that process natural language; and defines standard interfaces between
the different components of an NLP system.  It was designed primarily
to help teach graduate and undergraduate students about computational
linguistics; but it is also useful as a framework for implementing
research projects.

This package provides the Python 3 build of NLTK.

%prep
%setup -q -n %{mod_name}-%{version}

sed -i -e '/^#! *\//, 1d' %{mod_name}/corpus/reader/knbc.py \
                          %{mod_name}/test/runtests.py

%build
%{__python} setup.py build
%{__python3} setup.py build


%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{python_sitelib}/%{mod_name}/sentiment
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/%{python3_sitelib}/%{mod_name}/sentiment


%check
# skip tests since it requires nltk-data and a few utilities not available in
# Fedora
#%%{__python} %%{mod_name}/test/runtests.py
#%%{__python3} %%{mod_name}/test/runtests.py


%files
%doc LICENSE.txt INSTALL.txt
%{python_sitelib}/%{mod_name}
%{python_sitelib}/%{mod_name}-*.egg-info

%files -n python3-%{mod_name}
%doc LICENSE.txt INSTALL.txt
%{python3_sitelib}/%{mod_name}
%{python3_sitelib}/%{mod_name}-*.egg-info


%changelog
* Tue Mar 01 2016 Satoru SATOH <ssato@redhat.com> - 1:3.1-1
- Update to 3.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 03 2015 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:3.0.3-1
- Update to 3.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 24 2014 Robin Lee <cheeselee@fedoraproject.org> - 1:3.0.0-1
- Update to 3.0.0, build a python3 subpackage
- Drop the included distribute_setup.py
- License specified from 'ASL 2.0' to 'ASL 2.0 and GPLv2+ with exceptions'

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug  8 2013 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-5
- Update distribute_setup.py to work with setuptools >= 0.7

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-2
- BuildRequires:  python-setuptools

* Wed Dec 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-1
- Update to 2.0.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.1-0.6.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.1-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 12 2011 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.1-0.4.rc1
- Update to 2.0.1rc1
- Requires tkinter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-0.4.b9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Robin Lee <robinlee.sysu@gmail.com> - 1:2.0-0.3.b9
- update to 2.0b9

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:2.0-0.2.b8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 17 2010 Robin Lee <robinlee.sysu@gmail.com> - 1:2.0-0.1.b8
- Updated to 2.0b8
- License switched upstream to ASL 2.0 since 2.0b4
- Remove specifications for obsolete Fedora versions
- Remove python_sitelib definition
- URL and Source0 URL revised
- BuildRoot tag removed
- BR: tkinter removed, PyYAML added
- Requires: tkinter removed
- nltk-0.9.2-use-sys-yaml.patch removed
- All redundant commands in 'install' section removed
- nltk_contrib entry in 'file' section was removed since it will include no
  file. Upstream split off a new tarball for nltk-contrib.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:0.9.2-2
- Rebuild for Python 2.6

* Mon Apr  7 2008 Michel Salim <salimma@fedoraproject.org> - 1:0.9.2-1
- Update to 0.9.2

* Sat Feb 23 2008 Michel Salim <michel.sylvan@gmail.com> - 1:0.9-2
- Use system PyYAML (bug #432329)

* Sun Jan 20 2008 Michel Salim <michel.sylvan@gmail.com> - 1:0.9-1
- Update to final 0.9
- Add Epoch to clear upgrade path from (old) 1.4.4

* Sat Sep 22 2007 Michel Salim <michel.sylvan@gmail.com> - 0.9-0.2.b2
- BR on tkinter, it is now needed at build time

* Fri Sep 21 2007 Michel Salim <michel.sylvan@gmail.com> - 0.9-0.1.b2
- Updated to 0.9b2
- Renamed back to python-nltk

* Mon Dec 18 2006 Michel Salim <michel.salim@gmail.com> - 0.6.6-2
- Rebuild for development branch

* Mon Oct 30 2006 Michel Salim <michel.salim@gmail.com> - 0.6.6-1
- Initial package
