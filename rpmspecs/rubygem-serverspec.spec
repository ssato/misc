# Generated from serverspec-0.15.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name serverspec

Name:           rubygem-%{gem_name}
Version:        0.15.2
Release:        1%{?dist}
Summary:        RSpec tests for your servers configured by Puppet, Chef or anything else
Group:          Development/Languages
License:        MIT
URL:            http://serverspec.org
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:       ruby(release)
Requires:       ruby(rubygems) 
Requires:       rubygem(net-ssh) 
Requires:       rubygem(rspec) >= 2.13.0
Requires:       rubygem(highline) 
Requires:       rubygem(specinfra) >= 0.5.6
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel 
BuildRequires:  ruby 
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}

%description
RSpec tests for your servers configured by Puppet, Chef or anything else

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove unneeded files:
rm -f %{buildroot}%{gem_instdir}/.{gitignore,travis.yml}
rm -f %{buildroot}%{gem_instdir}/{Gemfile,Guardfile,Rakefile,WINDOWS_SUPPORT.md,serverspec.gemspec}
#rm -rf %{buildroot}%{gem_instdir}/spec/{aix,darwin,debian,freebsd,gentoo,plamo,smartos,solaris*,support,windows}/
find %{buildroot}%{gem_instdir}/spec -type f | sed "s,^%{buildroot},," > specs.list

%files -f specs.list
%dir %{gem_instdir}
%{_bindir}/serverspec-init
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files          doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/LICENSE.txt

%changelog
* Mon Feb 10 2014 Satoru SATOH <satoru.satoh@gmail.com> - 0.15.2-1
- Initial package
