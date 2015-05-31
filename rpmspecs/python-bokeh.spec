# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?fedora}
# NOTE: The upstream archive contains test and example code not runnable w/
# py3k. So disabled build for py3k for a while. (It seems that most of failures
# because of print statement not available in py3k so it's not pretty difficult
# to fix these but it takes some time, I guess.)
#%global with_python3 1
%global with_python3 0
%endif

%define debug_package %{nil}
%define pymodname bokeh

Name:           python-%{pymodname}
Version:        0.9.0
Release:        1%{?dist}
Summary:        A python interactive visualization library for large datasets that natively uses the latest web technologies
License:        BSD
Group:          Development/Languages
URL:            http://bokeh.pydata.org
Source0:        https://pypi.python.org/packages/source/b/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python
Requires:       python-dateutil
Requires:       python-flask
Requires:       python-jinja2
Requires:       python-markupsafe
Requires:       python-werkzeug
Requires:       python-gevent
Requires:       python-gevent-websocket
Requires:       python-greenlet
Requires:       python-itsdangerous
Requires:       numpy
Requires:       python-pandas
Requires:       python-dateutil
Requires:       pytz
Requires:       python-redis
Requires:       python-requests
Requires:       python-six
Requires:       python-wsgiref
Requires:       python-pygments
Requires:       pystache
Requires:       python-markdown
Requires:       python-tornado
Requires:       python-colorama
Requires:       python-zmq
Requires:       PyYAML
Requires:       redis
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
Bokeh is a Python interactive visualization library for large datasets that
natively uses the latest web technologies. Its goal is to provide elegant,
concise construction of novel graphics in the style of Protovis/D3, while
delivering high-performance interactivity over large data to thin clients.

%package        server
Summary:        Server for %{name}
Requires:       %{name} = %{version}-%{release}

%description    server
Bokeh is a Python interactive visualization library for large datasets that
natively uses the latest web technologies. Its goal is to provide elegant,
concise construction of novel graphics in the style of Protovis/D3, while
delivering high-performance interactivity over large data to thin clients.

This package contains server for %{name}.

%if 0%{?with_python3}
%package -n     python3-%{pymodname}
Summary:        A python interactive visualization library for large datasets that natively uses the latest web technologies
Requires:       python3
Requires:       python3-dateutil
Requires:       python3-flask
Requires:       python3-jinja2
Requires:       python3-markupsafe
Requires:       python3-werkzeug
Requires:       python3-gevent
Requires:       python3-gevent-websocket
Requires:       python3-greenlet
Requires:       python3-itsdangerous
Requires:       python3-numpy
Requires:       python3-pandas
Requires:       python3-dateutil
Requires:       python3-pytz
Requires:       python3-redis
Requires:       python3-requests
Requires:       python3-six
Requires:       python3-wsgiref
Requires:       python3-pygments
Requires:       python3-pystache
Requires:       python3-markdown
Requires:       python3-tornado
Requires:       python3-colorama
Requires:       python3-zmq
Requires:       python3-PyYAML

%description -n python3-%{pymodname}
Bokeh is a Python interactive visualization library for large datasets that
natively uses the latest web technologies. Its goal is to provide elegant,
concise construction of novel graphics in the style of Protovis/D3, while
delivering high-performance interactivity over large data to thin clients.

This is a package for python-3.
%endif

%prep
%setup -q -n %{pymodname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif
 
%files
%doc LICENSE.txt PKG-INFO examples
%{python_sitelib}/*

%files          server
%{_bindir}/*

%if 0%{?with_python3}
%files -n       python3-%{pymodname}
%defattr(644,root,root,755)
%doc LICENSE.txt PKG-INFO examples
%{python3_sitelib}/*
%endif

%changelog
* Sun May 31 2015 Satoru SATOH <ssato@redhat.com> - 0.9.0-1
- New upstream release

* Tue Mar 10 2015 Satoru SATOH <ssato@redhat.com> - 0.8.1-1
- Latest upstream release

* Mon Jan 13 2014 Satoru SATOH <ssato@redhat.com> - 0.3-1
- Initial packaging
