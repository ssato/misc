%global short_name      jett

Name:           java-%{short_name}
Version:        0.9.0
Release:        1%{?dist}
Summary:        Java Excel Template Translator
Group:          Development/Libraries
License:        LGPLv3
URL:            https://%{short_name}.sourceforge.net
Source0:        http://sourceforge.net/projects/jagg/files/%{version}/%{short_name}-%{version}-distr.zip
Patch0:         jett-0.9.0-parent-pomxml.patch
Patch1:         jett-0.9.0-hsqldb.patch
BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(net.sf.jagg:jagg-core)
BuildRequires:  mvn(org.apache.poi:poi)
BuildRequires:  mvn(org.apache.poi:poi-ooxml)
BuildRequires:  mvn(org.apache.commons:commons-jexl)
BuildRequires:  mvn(org.hsqldb:hsqldb)

%description
JETT is a Java 5.0 API that reads an Excel spreadsheet as a template, takes
your data, and creates a new Excel spreadsheet that contains your data,
formatted as in the template. It works with .xls and .xlsx template
spreadsheets.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}
%patch0 -p1 -b .parent
%patch1 -p1 -b .hsqldb
#%mvn_file  : %{short_name} %{name}
#%mvn_alias "hsqldb:hsqldb" "org.hsqldb:hsqldb"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc readme.txt

%files javadoc -f .mfiles-javadoc
%doc readme.txt

%changelog
* Mon Feb  9 2015 Satoru SATOH <ssato at redhat.com> - 0.9.0-1
- Initial package
