#
# Conditional build:
%bcond_without	static_libs	# static libraries

Summary:	Freeware Advanced Audio Decoder 2
Summary(pl.UTF-8):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	2.11.1
Release:	1
License:	GPL v2+
Group:		Applications/Sound
#Source0:	http://downloads.sourceforge.net/faac/%{name}-%{version}.tar.gz
#Source0Download: https://github.com/knik0/faad2/releases
Source0:	https://github.com/knik0/faad2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f85b2514c4fb2f87d22a3bc879d83277
Patch0:		%{name}-backward_compat.patch
URL:		https://github.com/knik0/faad2
BuildRequires:	cmake >= 3.15
BuildRequires:	rpmbuild(macros) >= 1.721
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%description -l pl.UTF-8
FAAD 2 to napisany całkowicie od początku dekoder MPEG2 i MPEG-4
obsługujący profile LC, MAIN i LTP.

%package libs
Summary:	FAAD 2 libraries
Summary(pl.UTF-8):	Biblioteki FAAD 2
Group:		Libraries
%if 0%{?_soname_prov:1}
Provides:	%{_soname_prov libfaad.so.0}
%endif
Conflicts:	faad2 < 2.0-3

%description libs
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. This package contains base FAAD 2
libraries: libfaad and libfaad_drm.

%description libs -l pl.UTF-8
FAAD 2 to napisany całkowicie od początku dekoder MPEG2 i MPEG-4
obsługujący profile LC, MAIN i LTP. Ten pakiet zawiera podstawowe
biblioteki FAAD 2: libfaad i libfaad_drm.

%package devel
Summary:	Header files for faad2
Summary(pl.UTF-8):	Pliki nagłówkowe faad2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for faad2.

%description devel -l pl.UTF-8
Pliki nagłówkowe faad2.

%package static
Summary:	Static faad2 library
Summary(pl.UTF-8):	Statyczna biblioteka faad2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static faad2 library.

%description static -l pl.UTF-8
Statyczna biblioteka faad2.

%prep
%setup -q
%patch0 -p1

%build
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C build-static
%endif

%cmake -B build

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

# ensure files from shared build are packaged
%{__rm} $RPM_BUILD_ROOT%{_bindir}/faad
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/faad2.pc
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# for compatibility with apps using dlopen("libfaad.so.0")
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libfaad.so.2.*.*) $RPM_BUILD_ROOT%{_libdir}/libfaad.so.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/faad
%{_mandir}/man1/faad.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libfaad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfaad.so.2
# compat symlink
%attr(755,root,root) %{_libdir}/libfaad.so.0
%attr(755,root,root) %{_libdir}/libfaad_drm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfaad_drm.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfaad.so
%attr(755,root,root) %{_libdir}/libfaad_drm.so
%{_includedir}/faad.h
%{_includedir}/neaacdec.h
%{_pkgconfigdir}/faad2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfaad.a
%{_libdir}/libfaad_drm.a
%endif
