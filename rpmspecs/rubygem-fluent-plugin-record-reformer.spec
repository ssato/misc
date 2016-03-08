%{?scl:%scl_package rubygems-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name fluent-plugin-record-reformer

%define _version 0.4.0
%define _summary "Fluentd plugin to add or replace fields of a event record" 
%define _url "https://github.com/sonots/fluent-plugin-record-reformer"
%define _license MIT

%define desc Fluentd plugin to add or replace fields of a event record

%if !("%{?scl}" == "ruby193" || 0%{?rhel} > 6 || 0%{?fedora} > 16)
%global gem_dir /usr/lib/ruby/gems/1.8
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%endif

Name:      %{?scl_prefix}rubygem-%{gem_name}
Version:   %{_version}
Release:   3%{?dist}  
Summary:   %{_summary}
Group:     Development/Languages
License:   %{_license}
URL:       %{_url}
Source0:   http://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch: noarch
Provides:  %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%if "%{?scl}" == "ruby193"
Requires: %{?scl_prefix}ruby-wrapper
BuildRequires: %{?scl_prefix}ruby-wrapper
%endif

%if 0%{?fedora} > 18  || 0%{?rhel} > 6
Requires: ruby(release) = 2.0.0
BuildRequires: ruby(release) = 2.0.0
BuildRequires: rubygems-devel
%else
%if "%{?scl}" == "ruby193" || 0%{?fedora} > 16
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
BuildRequires: %{?scl_prefix}ruby(abi) = 1.9.1
BuildRequires:  %{?scl_prefix}rubygems-devel
%else
Requires: ruby(abi) = 1.8
BuildRequires: ruby(abi) = 1.8
%endif
%endif
Requires: %{?scl_prefix}rubygems
BuildRequires: %{?scl_prefix}rubygems

%description
%{desc}

%package   doc
BuildArch: noarch
Requires:  %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:   Documentation for %{pkg_name}

%description doc
This package contains documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}
%setup -q -D -T -n %{gem_name}-%{version}

%{?scl:scl enable %{scl} "}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:"}

%build
%{?scl:scl enable %{scl} "}
gem build %{gem_name}.gemspec
%{?scl:"}

%if 0%{?fedora} > 18
%gem_install
%else
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install -V --local --install-dir .%{gem_dir} --force --rdoc \
    %{gem_name}-%{version}.gem
%{?scl:"}
%endif

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}

%files 
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/*.gemspec
%{gem_spec}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}/rdoc
%doc %{gem_docdir}/ri

%changelog
* Wed Mar 09 2016 Satoru SATOH <ssato@redhat.com> 0.4.0-1
- Initial experimental packaging
