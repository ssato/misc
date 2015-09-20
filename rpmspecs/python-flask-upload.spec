%global mod_name Flask-Uploads
%global with_python3 1

Name:           python-flask-uploads
Version:        0.1.3
Release:        1%{?dist}
Summary:        Flexible and efficient upload handling for Flask
Group:          Development/Libraries
License:        MIT
URL:            http://bitbucket.org/leafstorm/flask-uploads/
Source0:        http://pypi.python.org/packages/source/F/%{mod_name}/%{mod_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-flask
BuildRequires:  python-nose
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flask
BuildRequires:  python3-nose
# check can't work with python3 until builds for python3-flask-babel are available
#BuildRequires:  python3-flask-babel
%endif 

%description
Flask-Uploads provides flexible upload handling for Flask applications. It lets
you divide your uploads into sets that the application user can publish
separately.

%if 0%{?with_python3}
%package -n     python3-flask-uploads
Summary:        Flexible and efficient upload handling for Flask

%description -n python3-flask-uploads
Flask-Uploads provides flexible upload handling for Flask applications. It lets
you divide your uploads into sets that the application user can publish
separately.
%endif

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%doc README
%{python2_sitelib}/*.egg-info/
%{python2_sitelib}/Flask*
%{python2_sitelib}/flaskext

%if 0%{?with_python3}
%files       -n python3-flask-uploads
%doc README
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/Flask*
%{python3_sitelib}/flaskext
%endif


%changelog
* Sun Sep 20 2015 Satoru SATOH <ssato@redhat.com> - 0.1.3-1
- Initial RPM release
