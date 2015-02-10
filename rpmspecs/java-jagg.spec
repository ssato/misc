%global short_name      jagg

Name:           java-%{short_name}
Version:        0.9.0
Release:        2%{?dist}
Summary:        Java Aggregation operation library
Group:          Development/Libraries
License:        LGPLv3
URL:            https://%{short_name}.sourceforge.net
Source0:        http://sourceforge.net/projects/jagg/files/%{version}/%{short_name}-%{version}-distr.zip
Patch0:         jagg-0.9.0-parent-pomxml.patch
Patch1:         jagg-0.9.0-skip-some-tests.patch
BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)

%description
jAgg is a Java 5.0 API that supports "group by" operations on Lists of Java
objects: aggregate operations such as count, sum, max, min, avg, and many more.
It supports Super Aggregation: Rollups, Cube, and Grouping Sets. It supports
analytic operations such as lag/lead and row number and more. It also allows
custom aggregate and analytic operations.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}
%patch0 -p1 -b .parent
%patch1 -p1 -b .skip
# see also: https://fedorahosted.org/released/javapackages/doc/#mvn_file
#%mvn_file  :%{short_name}-core %{short_name}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc readme.txt

%files javadoc -f .mfiles-javadoc
%doc readme.txt

%changelog
* Mon Feb  9 2015 Satoru SATOH <ssato at redhat.com> - 0.9.0-2
- Fix Url

* Mon Feb  9 2015 Satoru SATOH <ssato at redhat.com> - 0.9.0-1
- Initial package
