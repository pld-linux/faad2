#
# Conditional build:
# _without_xmms		- without XMMS plugin
#
Summary:	Freeware Advanced Audio Decoder 2
Summary(pl):	Darmowy zaawansowany dekoder audio
Name:		faad2
Version:	1.1
Release:	2
License:	GPL
Group:		Libraries
Source0:	http://faac.sourceforge.net/files/%{name}-%{version}.tar.gz
Patch0:		%{name}-libsndfile.patch
URL:		http://www.audiocoding.com/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_xmms:BuildRequires:	id3lib-devel >= 3.8.2 }
BuildRequires:	libsndfile-devel >= 1.0.4
BuildRequires:	libtool
%{!?_without_xmms:BuildRequires:	xmms-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if 0%{!?_without_xmms:1}
%define		_xmms_plugin_dir	%(xmms-config --input-plugin-dir)
%endif

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

%description -n xmms-input-faad2
XMMS plugin for AAC files.

%description -n xmms-input-faad2 -l pl
Wtyczka XMMS do plików AAC.

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

%if 0%{!?_without_xmms:1}
cd plugins/xmms
%{__cc} -shared -fPIC -o libaac-XMMS.so aac-XMMS.c \
	`xmms-config --cflags --libs` \
	-I../../include \
	-L../../libfaad/.libs -lfaad -lid3 -lz
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0%{!?_without_xmms:1}
install -d $RPM_BUILD_ROOT%{_xmms_plugin_dir}
install plugins/xmms/libaac-XMMS.so $RPM_BUILD_ROOT%{_xmms_plugin_dir}
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

%if 0%{!?_without_xmms:1}
%files -n xmms-input-faad2
%defattr(644,root,root,755)
%attr(755,root,root) %{_xmms_plugin_dir}/*.so
%endif
