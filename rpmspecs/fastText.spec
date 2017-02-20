%global date_rev  201702211
%global git_rev   ded69eb

Name:           fastText
Version:        %{date_rev}
Release:        1.git.%{git_rev}%{?dist}
Summary:        Library for fast text representation and classification
Group:          Development/Libraries
License:        BSD
URL:            https://github.com/facebookresearch/fastText
## Git version:
# Fetch git HEAD version and make an archive:
# git clone -b master git://github.com/facebookresearch/fastText fastText-%{date_rev} && \
#     rm -rf fastText-%{date_rev}/.git* && \
#     tar --xz -cvf fastText-%{date_rev}.tar.xz fastText-%{date_rev}
#Source0:        %{name}-%{date_rev}.tar.xz
Source0:        %{name}-%{version}.tar.xz
Patch0:         fastText-install.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires:  ...

%description
fastText is a library for efficient learning of word representations and
sentence classification.

%prep
%setup -q -n %{name}-%{date_rev}
%patch0 -p1 -b .inst

%build
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%doc README.md CONTRIBUTING.md PATENTS wikifil.pl eval.py word-vector-example.sh classification-example.sh classification-results.sh
%{_bindir}/*

%changelog
* Tue Feb 21 2017 Satoru SATOH <ssato@redhat.com> - 201702211-1.git.ded69eb
- Initial package.
