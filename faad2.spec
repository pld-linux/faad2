#
# Conditional build:
%bcond_without	mpeg4ip		# build without mp4v2 support in decoder
				# ...and don't build XMMS or MPEG4IP plugins
%bcond_without	xmms		# don't build XMMS plugin
%bcond_with	bootstrap	# bootstrap (alias for _without_mpeg4ip)
#
%{?with_bootstrap:%undefine with_mpeg4ip}
%{!?with_mpeg4ip:%undefine with_xmms}
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	2.0
Release:	3
License:	GPL
Group:		Applications/Sound
Source0:	http://dl.sourceforge.net/faac/%{name}-%{version}.tar.gz
# Source0-md5:	1a6f79365f2934a4888b210ef47a3a07
Patch0:		%{name}-make.patch
Patch1:		%{name}-mp4v2.patch
URL:		http://www.audiocoding.com/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_xmms:BuildRequires:	id3lib-devel >= 3.8.2}
BuildRequires:	libtool >= 2:1.4d-3
%{?with_mpeg4ip:BuildRequires:	mpeg4ip-devel >= 1.0}
%{?with_xmms:Buildrequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%description -l pl
FAAD 2 to napisany ca³kowicie od pocz±tku dekoder MPEG2 i MPEG-4
obs³uguj±cy profile LC, MAIN i LTP.

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
FAAD 2 to napisany ca³kowicie od pocz±tku dekoder MPEG2 i MPEG-4
obs³uguj±cy profile LC, MAIN i LTP. Ten pakiet zawiera podstawowe
biblioteki FAAD 2: libfaad i libmp4ff.

%package devel
Summary:	Header files for faad2
Summary(pl):	Pliki nag³ówkowe faad2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for faad2.

%description devel -l pl
Pliki nag³ówkowe faad2.

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
Summary(pl):	Wtyczka MPEG4IP do plików AAC
Group:		Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mpeg4ip

%description -n mpeg4ip-plugin-faad2
MPEG4IP plugin for AAC files.

%description -n mpeg4ip-plugin-faad2 -l pl
Wtyczka MPEG4IP do plików AAC.

%package -n xmms-input-faad2
Summary:	XMMS plugin for AAC files
Summary(pl):	Wtyczka XMMS do plików AAC
Group:		X11/Applications/Sound
Requires:	%{name}-libs = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl
Wtyczka XMMS do plików AAC.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_xmms:--with-xmms}

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
%attr(755,root,root) %{_libdir}/libmp4ff.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfaad.so
%attr(755,root,root) %{_libdir}/libmp4ff.so
%{_libdir}/libfaad.la
%{_libdir}/libmp4ff.la
%{_includedir}/faad.h
%{_includedir}/mp4ff.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libfaad.a
%{_libdir}/libmp4ff.a

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
