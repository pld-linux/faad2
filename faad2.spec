#
# Conditional build:
%bcond_with	bootstrap	# bootstrap (alias for _without_mpeg4ip)
%bcond_with	mpeg4ip		# don't build MPEG4IP plugin
%bcond_without	static_libs	# don't build static libraries
%bcond_without	xmms		# don't build XMMS plugin

%{?with_bootstrap:%undefine with_mpeg4ip}
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl.UTF-8):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	2.8.8
Release:	1
License:	GPL v2+
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/faac/%{name}-%{version}.tar.gz
# Source0-md5:	28f6116efdbe9378269f8a6221767d1f
Patch0:		%{name}-make.patch
Patch1:		%{name}-mpeg4ip.patch
Patch3:		%{name}-backward_compat.patch
Patch4:		%{name}-mp4ff.patch
Patch6:		%{name}-mp4v2.patch
URL:		http://www.audiocoding.com/
%{?with_mpeg4ip:BuildRequires:	SDL-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_xmms:BuildRequires:	id3lib-devel >= 3.8.2}
BuildRequires:	libtool >= 2:1.4d-3
%if %{with mpeg4ip}
BuildRequires:	mp4v2-devel
BuildRequires:	mpeg4ip-devel >= 1:1.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.721
%{?with_xmms:BuildRequires:	xmms-devel}
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
libraries: libfaad and libmp4ff.

%description libs -l pl.UTF-8
FAAD 2 to napisany całkowicie od początku dekoder MPEG2 i MPEG-4
obsługujący profile LC, MAIN i LTP. Ten pakiet zawiera podstawowe
biblioteki FAAD 2: libfaad i libmp4ff.

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

%package -n mpeg4ip-plugin-faad2
Summary:	MPEG4IP plugin for AAC files
Summary(pl.UTF-8):	Wtyczka MPEG4IP do plików AAC
Group:		Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mpeg4ip

%description -n mpeg4ip-plugin-faad2
MPEG4IP plugin for AAC files.

%description -n mpeg4ip-plugin-faad2 -l pl.UTF-8
Wtyczka MPEG4IP do plików AAC.

%package -n xmms-input-faad2
Summary:	XMMS plugin for AAC files
Summary(pl.UTF-8):	Wtyczka XMMS do plików AAC
Group:		X11/Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl.UTF-8
Wtyczka XMMS do plików AAC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with%{!?with_xmms:out}-xmms \
	--with%{!?with_mpeg4ip:out}-mpeg4ip \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with xmms}
%{__rm} $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.{la,a}
%endif
%if %{with mpeg4ip}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{la,a}
%endif

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
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libfaad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfaad.so.2
# compat symlink
%attr(755,root,root) %{_libdir}/libfaad.so.0
%attr(755,root,root) %{_libdir}/libfaad_drm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfaad_drm.so.2
%attr(755,root,root) %{_libdir}/libmp4ff.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp4ff.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfaad.so
%attr(755,root,root) %{_libdir}/libfaad_drm.so
%attr(755,root,root) %{_libdir}/libmp4ff.so
%{_libdir}/libfaad.la
%{_libdir}/libfaad_drm.la
%{_libdir}/libmp4ff.la
%{_includedir}/faad.h
%{_includedir}/mp4ff.h
%{_includedir}/mp4ffint.h
%{_includedir}/neaacdec.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfaad.a
%{_libdir}/libfaad_drm.a
%{_libdir}/libmp4ff.a
%endif

%if %{with xmms}
%files -n xmms-input-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/libmp4.so
%endif

%if %{with mpeg4ip}
%files -n mpeg4ip-plugin-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mp4player_plugin/faad2_plugin.so*
%endif
