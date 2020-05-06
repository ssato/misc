# https://fedoraproject.org/wiki/Packaging:Ruby

%global gem_name asciidoctor-pdf-cjk
%define pre %nil

Summary: Asciidoctor PDF CJK extension
Name: rubygem-%{gem_name}
Version: 0.1.3
Release: 2%{?dist}
License: MIT
URL: https://github.com/chloerei/asciidoctor-pdf-cjk
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{pre}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
BuildArch: noarch
Provides: %{gem_name} = %{version}

%if %{?pre:1}
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}%{pre}
%global gem_cache   %{gem_dir}/cache/%{gem_name}-%{version}%{pre}.gem
%global gem_spec    %{gem_dir}/specifications/%{gem_name}-%{version}%{pre}.gemspec
%global gem_docdir  %{gem_dir}/doc/%{gem_name}-%{version}%{pre}
%endif

%description
A CJK extension fo Asciidoctor PDF

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack -V %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version}%{pre}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Hack!
sed -i.save -r 's/~> 1.5.0.alpha.8/>= 0/g' %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install -n %{gem_name}-%{version}%{pre}.gem

%check
pushd .%{gem_instdir}
LANG=C.UTF-8 ruby -I"lib:test" -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%install
mkdir -p %{buildroot}%{gem_dir}
# find .%{gem_dir}/gems/*/lib -type f -exec chmod -x {} \;
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/*.gemspec
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/bin
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/README.*
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Wed May  6 2020 Satoru SATOH <satoru.satoh@gmail.com> - 0.1.3-2
- Drop rhel7 support

* Fri May 24 2019 Satoru SATOH <ssato@redhat.com> - 0.1.3-1
- Initial package
