Summary:	MATE screensaver
Name:		mate-screensaver
Version:	1.8.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	a392fefa7d00f25c10e526d2dbd0d25a
Source1:	%{name}.pamd
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	intltool
BuildRequires:	libexif-devel
BuildRequires:	libmatekbd-devel
BuildRequires:	libtool
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-menus-devel
BuildRequires:	pam-devel
BuildRequires:	pkg-config
BuildRequires:	systemd-devel
BuildRequires:	xmlto
BuildRequires:	yelp-tools
Requires(post,preun):	glib-gio-gsettings
Requires:	xdg-menus
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
A new screensaver solution for MATE, with better HIG dialogs and a
much better integration into the desktop than the old xscreensaver.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/MateConf
%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/screensavers/gnomelogo-floaters.desktop
%{__rm} $RPM_BUILD_ROOT%{_pixmapsdir}/gnome-logo-white.svg

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/mate-screensaver

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/mate-screensaver
%attr(755,root,root) %{_bindir}/mate-screensaver
%attr(755,root,root) %{_bindir}/mate-screensaver-command
%attr(755,root,root) %{_bindir}/mate-screensaver-preferences
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mate-screensaver-dialog
%attr(755,root,root) %{_libexecdir}/mate-screensaver-gl-helper
%dir %{_libexecdir}/mate-screensaver
%attr(755,root,root) %{_libexecdir}/mate-screensaver/floaters
%attr(755,root,root) %{_libexecdir}/mate-screensaver/popsquares
%attr(755,root,root) %{_libexecdir}/mate-screensaver/slideshow
%{_datadir}/backgrounds/cosmos
%{_datadir}/dbus-1/services/org.mate.ScreenSaver.service
%{_datadir}/desktop-directories/mate-screensaver.directory
%{_datadir}/glib-2.0/schemas/org.mate.screensaver.gschema.xml
%{_datadir}/mate-background-properties/cosmos.xml
%{_datadir}/mate-screensaver
%{_desktopdir}/mate-screensaver-preferences.desktop
%{_desktopdir}/screensavers/cosmos-slideshow.desktop
%{_desktopdir}/screensavers/footlogo-floaters.desktop
%{_desktopdir}/screensavers/personal-slideshow.desktop
%{_desktopdir}/screensavers/popsquares.desktop
%{_pixmapsdir}/*.svg
%{_sysconfdir}/xdg/autostart/mate-screensaver.desktop
%{_sysconfdir}/xdg/menus/mate-screensavers.menu
%{_mandir}/man1/*.1*

