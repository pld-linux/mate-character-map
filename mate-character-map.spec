#
# Conditional build:
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x
%bcond_with	static_libs	# static library
#
Summary:	Unicode character map (MATE version)
Summary(pl.UTF-8):	Mapa znaków unikodowych (wersja dla MATE)
Name:		mate-character-map
Version:	1.6.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	3ce6af1f3d359e595c2f842acf9237b8
Patch0:		%{name}-doc.patch
Patch1:		%{name}-python.patch
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gnome-doc-utils >= 0.12.2
BuildRequires:	gobject-introspection-devel >= 0.10.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.14.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils >= 0.9.0
BuildRequires:	pkgconfig
%{!?with_gtk3:BuildRequires:	python-devel >= 1:2.4}
%{!?with_gtk3:BuildRequires:	python-pygtk-devel >= 2:2.7.1}
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	scrollkeeper
Requires:	%{name}-libs = %{version}-%{release}
Conflicts:	mucharmap
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mucharmap is a featureful unicode character map. It's a fork of
gucharmap.

%description -l pl.UTF-8
Mucharmap jest wartościową mapą znaków unikodowych. Jest to
odgałęzienie pakietu gucharmap.

%package libs
Summary:	mucharmap library for MATE
Summary(pl.UTF-8):	Biblioteka mucharmap dla MATE
Group:		X11/Libraries
Requires:	glib2 >= 1:2.26.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.14.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}

%description libs
This package contains mucharmap library.

%description libs -l pl.UTF-8
Pakiet ten zawiera bibliotekę mucharmap.

%package devel
Summary:	Headers for mucharmap
Summary(pl.UTF-8):	Pliki nagłówkowe mucharmap
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.14.0}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0.0}

%description devel
The mucharmap-devel package includes the header files that you will
need to use mucharmap.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do kompilacji programów
używających mucharmap.

%package static
Summary:	Static mucharmap library
Summary(pl.UTF-8):	Statyczna biblioteka mucharmap
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of mucharmap library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki mucharmap.

%package apidocs
Summary:	mucharmap library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki mucharmap
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mucharmap library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki mucharmap.

%package -n python-mucharmap
Summary:	Python binding for mucharmap library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki mucharmap
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk >= 2:2.7.1

%description -n python-mucharmap
Python binding for mucharmap library.

%description -n python-mucharmap -l pl.UTF-8
Wiązanie Pythona do biblioteki mucharmap.

%package -n python-mucharmap-devel
Summary:	Development files for mucharmap Python binding
Summary(pl.UTF-8):	Pliki programistyczne wiązania Pythona do biblioteki mucharmap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-pygtk-devel >= 2:2.7.1

%description -n python-mucharmap-devel
Development files for mucharmap Python binding.

%description -n python-mucharmap-devel -l pl.UTF-8
Pliki programistyczne wiązania Pythona do biblioteki mucharmap.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mate-doc-prepare --copy --force
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-scrollkeeper \
	--disable-silent-rules \
	--enable-gtk-doc \
	--enable-introspection \
	--enable-python-bindings \
	%{!?with_static_libs:--disable-static} \
	%{?with_gtk3:--with-gtk=3.0} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{without gtk3}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/*.a
%endif
%endif

%find_lang mucharmap --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%scrollkeeper_update_post

%postun
%glib_compile_schemas
%scrollkeeper_update_postun

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f mucharmap.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING.UNICODE ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mucharmap
%attr(755,root,root) %{_bindir}/mate-character-map
%{_datadir}/glib-2.0/schemas/org.mate.mucharmap.*.xml
%{_desktopdir}/mucharmap.desktop

%files libs
%defattr(644,root,root,755)
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/libmucharmap-2.90.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmucharmap-2.90.so.7
%{_libdir}/girepository-1.0/Mucharmap-2.90.typelib
%else
%attr(755,root,root) %{_libdir}/libmucharmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmucharmap.so.7
%{_libdir}/girepository-1.0/Mucharmap-2.0.typelib
%endif

%files devel
%defattr(644,root,root,755)
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/libmucharmap-2.90.so
%{_includedir}/mucharmap-2.90
%{_pkgconfigdir}/mucharmap-2.90.pc
%{_datadir}/gir-1.0/Mucharmap-2.90.gir
%else
%attr(755,root,root) %{_libdir}/libmucharmap.so
%{_includedir}/mucharmap-2.0
%{_pkgconfigdir}/mucharmap-2.pc
%{_datadir}/gir-1.0/Mucharmap-2.0.gir
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%if %{with gtk3}
%{_libdir}/libmucharmap-2.90.a
%else
%{_libdir}/libmucharmap.a
%endif
%endif

%files apidocs
%defattr(644,root,root,755)
%if %{with gtk3}
%{_gtkdocdir}/mucharmap-2.90
%else
%{_gtkdocdir}/mucharmap-2.0
%endif

%if %{without gtk3}
%files -n python-mucharmap
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/gtk-2.0/mucharmap.so

%files -n python-mucharmap-devel
%defattr(644,root,root,755)
%{_datadir}/pygtk/2.0/defs/mucharmap.defs
%endif
