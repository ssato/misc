%global srcname VK_API_VERSION
%global txzname Vulkan-%{srcname}

Name:           vulkan-api-demos
Version:        105
Release:        1%{?dist}
Summary:        Vulkan examples and demos
License:        MIT
URL:            https://github.com/SaschaWillems/Vulkan
Source0:        %{url}/archive/%{srcname}_%{version}.tar.gz
Requires:       assimp
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-xrm-devel
BuildRequires:  vulkan-devel
BuildRequires:  assimp-devel

%description
Assorted C++ examples for Vulkan(tm), the new graphics and compute API from
Khronos.

%prep
%autosetup -p1 -n %{txzname}_%{version}
mkdir build

%build
pushd build
  %cmake ..
  %make_build
popd

%install
pushd build
  rm -f bin/assimp*.dll
  install -d $RPM_BUILD_ROOT/%{_bindir}
  for x in bin/*; do install -m 755 $x  $RPM_BUILD_ROOT/%{_bindir}; done
popd

#%check
#pushd build
#  ctest -VV
#popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.md
%doc README.md
%{_bindir}/*

%changelog
* Mon Jan 23 2017 Satoru SATOH <ssato@redhat.com> - 105-1
- Initial packaging
