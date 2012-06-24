#
# Conditional build:
%bcond_with	bootstrap	# bootstrap (alias for _without_mpeg4ip)
%bcond_without	mpeg4ip		# don't build MPEG4IP plugin
%bcond_without	static_libs	# don't build static libraries
%bcond_without	xmms		# don't build XMMS plugin
#
%{?with_bootstrap:%undefine with_mpeg4ip}
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	2.5
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	http://dl.sourceforge.net/faac/%{name}-%{version}.tar.gz
# Source0-md5:	696490935bf65b2ace4aafaff79e2396
Patch0:		%{name}-make.patch
Patch1:		%{name}-no-extension.patch
Patch2:		%{name}-mpeg4ip.patch
Patch3:		%{name}-inttypes_h.patch
URL:		http://www.audiocoding.com/
%{?with_mpeg4ip:BuildRequires:	SDL-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_xmms:BuildRequires:	id3lib-devel >= 3.8.2}
BuildRequires:	libtool >= 2:1.4d-3
%{?with_mpeg4ip:BuildRequires:	mpeg4ip-devel >= 1:1.5}
%{?with_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%description -l pl
FAAD 2 to napisany ca�kowicie od pocz�tku dekoder MPEG2 i MPEG-4
obs�uguj�cy profile LC, MAIN i LTP.

%package libs
Summary:	FAAD 2 libraries
Summary(pl):	Biblioteki FAAD 2
Group:		Libraries
Conflicts:	faad2 < 2.0-3

%description libs
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch. This package contains base FAAD 2
libraries: libfaad and libmp4ff.

%description libs -l pl
FAAD 2 to napisany ca�kowicie od pocz�tku dekoder MPEG2 i MPEG-4
obs�uguj�cy profile LC, MAIN i LTP. Ten pakiet zawiera podstawowe
biblioteki FAAD 2: libfaad i libmp4ff.

%package devel
Summary:	Header files for faad2
Summary(pl):	Pliki nag��wkowe faad2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for faad2.

%description devel -l pl
Pliki nag��wkowe faad2.

%package static
Summary:	Static faad2 library
Summary(pl):	Statyczna biblioteka faad2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static faad2 library.

%description static -l pl
Statyczna biblioteka faad2.

%package -n mpeg4ip-plugin-faad2
Summary:	MPEG4IP plugin for AAC files
Summary(pl):	Wtyczka MPEG4IP do plik�w AAC
Group:		Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mpeg4ip

%description -n mpeg4ip-plugin-faad2
MPEG4IP plugin for AAC files.

%description -n mpeg4ip-plugin-faad2 -l pl
Wtyczka MPEG4IP do plik�w AAC.

%package -n xmms-input-faad2
Summary:	XMMS plugin for AAC files
Summary(pl):	Wtyczka XMMS do plik�w AAC
Group:		X11/Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl
Wtyczka XMMS do plik�w AAC.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

rm -f $RPM_BUILD_ROOT%{xmms_input_plugindir}/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/mp4player_plugin/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/faad

%files libs
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libfaad.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfaad.so
%{_libdir}/libfaad.la
%{_includedir}/faad.h
%{_includedir}/neaacdec.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfaad.a
%endif

%if %{with xmms}
%files -n xmms-input-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%endif

%if %{with mpeg4ip}
%files -n mpeg4ip-plugin-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mp4player_plugin/*.so*
%endif
