%global short_name      xlsbeans

Name:           java-%{short_name}
Version:        1.2.5
Release:        2%{?dist}
Summary:        Java library for mapping Excel sheets to POJO
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/takezoe/%{short_name}
Source0:        https://github.com/takezoe/%{short_name}/archive/%{version}.tar.gz
Patch0:         xlsbeans-1.2.5-build-w-apache-commons-ognl.patch
Patch1:         xlsbeans-1.2.5-avoid-build-failure-of-date-format-mismatch.patch
Patch2:         xlsbeans-1.2.5-explicitly-set-char-encoding-for-build.patch
BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.tukaani:xz)
BuildRequires:  mvn(net.sourceforge.jexcelapi:jxl)
BuildRequires:  mvn(org.apache.poi:poi)
BuildRequires:  mvn(org.apache.poi:poi-ooxml)
BuildRequires:  mvn(org.apache.commons:commons-ognl)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-ssh)

%description
XLSBeans is a Java library for mapping Excel sheets to POJO.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}
# NOTE: Is it possible to pass the path of pom.xml to pom_change_dep ?
#%pom_change_dep ognl:ognl org.apache.commons:commons-ognl
%patch0 -p1 -b .ognl
%patch1 -p1 -b .datefmt
%patch2 -p1 -b .utf-8

%build
%mvn_file  : %{short_name} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE README.md excel.png

%files javadoc -f .mfiles-javadoc
%doc LICENSE README.md excel.png

%changelog
* Mon Feb  9 2015 Satoru SATOH <ssato at redhat.com> - 1.2.5-2
- Clean up RPM SPEC

* Mon Feb  9 2015 Satoru SATOH <ssato at redhat.com> - 1.2.5-1
- Initial package
