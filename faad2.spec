#
# Conditional build:
%bcond_without	xmms	# without XMMS plugin
#
%define		_rc rc3
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	2.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/faac/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	0080076438655ed7facf1089a9805aff
URL:		http://www.audiocoding.com/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_xmms:BuildRequires:	id3lib-devel >= 3.8.2 }
BuildRequires:	libsndfile-devel >= 1.0.4
BuildRequires:	libtool
%{!?_without_xmms:Buildrequires:	rpmbuild(macros) >= 1.125}
%{!?_without_xmms:BuildRequires:	xmms-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder,
completely written from scratch.

%description -l pl
FAAD 2 to napisany ca³kowicie od pocz±tku dekoder MPEG2 i MPEG-4
obs³uguj±cy profile LC, MAIN i LTP.

%package devel
Summary:	Devel files for faad2
Summary(pl):	Pliki nag³ówkowe faad2
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Devel files for faad2.

%description devel -l pl
Pliki nag³ówkowe faad2.

%package static
Summary:	Static faad2 library
Summary(pl):	Statyczna biblioteka faad2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static faad2 library.

%description static -l pl
Statyczna biblioteka faad2.

%package -n xmms-input-faad2
Summary:	XMMS plugin for AAC files
Summary(pl):	Wtyczka XMMS do plików AAC
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}
Requires:	xmms

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl
Wtyczka XMMS do plików AAC.

%prep
%setup -q -n %{name}

%build
sh ./bootstrap
%configure
%{__make}

%if %{with xmms}
%{__make} -C plugins/xmms \
	GTK_CONFIG=gtk-config
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with xmms}
%{__make} \
	-C plugins/xmms \
	install \
	GTK_CONFIG=gtk-config \
	DESTDIR=$RPM_BUILD_ROOT
%endif

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

%if %{with xmms}
%files -n xmms-input-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%endif
