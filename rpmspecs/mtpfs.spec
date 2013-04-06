Name:           mtpfs
Version:        1.1
Release:        1%{?dist}
Summary:        FUSE filesystem to access MTP device with libmtp
License:        GPLv3
URL:            http://www.adebenham.com/mtpfs
Source0:        http://www.adebenham.com/files/mtp/%{name}-%{version}.tar.gz
BuildRequires:  fuse-devel
BuildRequires:  libid3tag-devel
BuildRequires:  libmtp-devel
BuildRequires:  libmad-devel
Requires:       fuse
#Requires:       libmtp
#Requires:       libmad
#Requires:       libid3tag


%description
MTPFS is a FUSE filesystem based on libmtp that allows a mtp device to be
browsed as if it were a normal external harddisk.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/*


%changelog
* Thu Apr 19 2012 Satoru SATOH <ssato@redhat.com> - 1.1-1
- Initial packaging.
