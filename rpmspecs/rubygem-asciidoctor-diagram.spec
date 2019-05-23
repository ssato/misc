# https://fedoraproject.org/wiki/Packaging:Ruby

%global gem_name asciidoctor-diagram
%define pre %nil

Summary: A set of Asciidoctor extensions to add diagrams
Name: rubygem-%{gem_name}
Version: 1.5.16
Release: 1%{?dist}
License: MIT
URL: https://github.com/asciidoctor/asciidoctor-diagram
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{pre}.gem
%if 0%{?el7}
Requires: ruby(release)
BuildRequires: ruby(release)
%endif
BuildRequires: rubygems-devel
BuildRequires: ruby(rubygems)
BuildArch: noarch
Provides: %{gem_name} = %{version}
%if 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%if %{?pre:1}
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}%{pre}
%global gem_cache   %{gem_dir}/cache/%{gem_name}-%{version}%{pre}.gem
%global gem_spec    %{gem_dir}/specifications/%{gem_name}-%{version}%{pre}.gemspec
%global gem_docdir  %{gem_dir}/doc/%{gem_name}-%{version}%{pre}
%endif

%description
Asciidoctor diagram extension, with support for AsciiToSVG, BlockDiag
(BlockDiag, SeqDiag, ActDiag, NwDiag), Ditaa, Erd, GraphViz, Mermaid, Msc,
PlantUML, Shaape, SvgBob, Syntrax, UMLet, Vega, Vega-Lite and WaveDrom. 

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

%build
gem build %{gem_name}.gemspec
%gem_install -n %{gem_name}-%{version}%{pre}.gem

%check
pushd .%{gem_instdir}
%if 0%{?el7}
%else
LANG=C.UTF-8 ruby -I"lib:test" -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%endif
popd

%install
mkdir -p %{buildroot}%{gem_dir}
find .%{gem_dir}/gems/*/lib -type f -exec chmod -x {} \;
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/spec
%exclude %{gem_instdir}/Rakefile
%license %{gem_instdir}/LICENSE.txt
%doc %{gem_instdir}/CHANGELOG.adoc
%doc %{gem_instdir}/README.*
%lang(zh_CN) %doc %{gem_instdir}/README_zh-CN.*
%{gem_instdir}/examples
%{gem_instdir}/images
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu May 23 2019 Satoru SATOH <ssato@redhat.com> - 1.5.16-1
- Initial package
