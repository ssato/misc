# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           trac-ganttcalendar-plugin
Version:        0.6.2
Release:        1%{?dist}
Summary:        Ticket Gantt chart and calendar plugin for Trac
Group:          Applications/Internet
License:        BSD
URL:            http://trac-hacks.org/wiki/GanttCalendarPlugin
#
# Source comes from git repo:
#  git clone git://recursive-design.com/gantt-calendar.git
#  cd gantt-calendar && python setup.py sdist --formats bztar
#
Source0:        TracGanttCalendarPlugin-%{version}.tar.bz2
#Source1:        README.textile
#Source2:        README.ja.textile
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       trac >= 0.12, python-setuptools


%description
The GanttCalendar plugin adds ticket Gantt chart and calendar functionality to
Trac. It is licensed under the new BSD license .


%prep
%setup -n TracGanttCalendarPlugin-%{version} -q


%build
%{__python} setup.py build
#cp $RPM_SOURCE_DIR/%{SOURCE1} $RPM_SOURCE_DIR/%{SOURCE2} ./


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
## FIXME:
#%doc README.ja.textile README.textile
%{python_sitelib}/*


%changelog
* Tue Sep 25 2012 Satoru SATOH <ssato@redhat.com> - 0.6.2-1
- New upstream

* Sun Dec 05 2010 Satoru SATOH <satoru.satoh+github@gmail.com> - 0.1.0-1
- Initial build
