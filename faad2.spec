# TODO:
# - xmms plugin
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	1.1
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://faac.sourceforge.net/files/%{name}-%{version}.tar.gz
Patch0:		%{name}-libsndfile.patch
URL:		http://www.audiocoding.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libsndfile-devel >= 1.0.4
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%package devel
Summary:	Devel files for faad2
Group:		Development/Libraries

%description devel
Devel files for faad2.

%package static
Summary:	Static faad2 library
Group:		Development/Libraries

%description static
Static faad2 library.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
