# Generated from travis-1.6.17.gem by gem2rpm -*- rpm-spec -*-
%global gem_name travis

Name: rubygem-%{gem_name}
Version: 1.6.17
Release: 1%{?dist}
Summary: Travis CI client
Group: Development/Languages
License: MIT
URL: https://github.com/travis-ci/travis.rb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems) 
Requires: rubygem(faraday) => 0.9
Requires: rubygem(faraday) < 1
Requires: rubygem(faraday_middleware) => 0.9
Requires: rubygem(faraday_middleware) < 1
Requires: rubygem(faraday_middleware) >= 0.9.1
Requires: rubygem(highline) => 1.6
Requires: rubygem(highline) < 2
Requires: rubygem(backports) 
Requires: rubygem(gh) => 0.13
Requires: rubygem(gh) < 1
Requires: rubygem(launchy) => 2.1
Requires: rubygem(launchy) < 3
Requires: rubygem(pry) < 0.10
Requires: rubygem(pry) => 0.9
Requires: rubygem(pry) < 1
Requires: rubygem(typhoeus) => 0.6
Requires: rubygem(typhoeus) < 1
Requires: rubygem(typhoeus) >= 0.6.8
Requires: rubygem(pusher-client) => 0.4
Requires: rubygem(pusher-client) < 1
Requires: rubygem(addressable) => 2.3
Requires: rubygem(addressable) < 3
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby 
# BuildRequires: rubygem(rspec) => 2.12
# BuildRequires: rubygem(rspec) < 3
# BuildRequires: rubygem(sinatra) => 1.3
# BuildRequires: rubygem(sinatra) < 2
# BuildRequires: rubygem(rack-test) => 0.6
# BuildRequires: rubygem(rack-test) < 1
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
CLI and Ruby client library for Travis CI.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Run the test suite
%check
pushd .%{gem_instdir}

popd

%files
%dir %{gem_instdir}
%{_bindir}/travis
#%{gem_instdir}/bin
%{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Aug 01 2014 Satoru SATOH - 1.6.17-1
- Initial package
