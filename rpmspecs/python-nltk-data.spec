Name:           python-nltk-data
Version:        20170315
Release:        1%{?dist}
Summary:        NLTK corpora data
Group:          Development/Libraries
License:        Commercial
URL:            http://www.nltk.org/nltk_data/
# 1. python: import nltk; nltk.download()
# 2. make an archive:
#   d=/path/to/workdir/python-nltk-data-$(date +%Y%m%d)
#   mv ~/nltk_data ${d}
#   cd /path/to/workdir
#   tar --xz -cvf ${d##*/}.tar.xz ${d##*/}
Source0:        %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       python-nltk

%description
NLTK Corpora data available from %{url}.

%prep
%setup -q

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nltk_data/
cp -a ./* $RPM_BUILD_ROOT%{_datadir}/nltk_data/

%files
%defattr(-,root,root,-)
%{_datadir}/nltk_data/

%changelog
* Wed Mar 15 2017 Satoru SATOH <ssato@redhat.com> - 20170315-1
- Update data

* Mon Feb 29 2016 Satoru SATOH <ssato@redhat.com> - 20160229-1
- Initial packaging.
