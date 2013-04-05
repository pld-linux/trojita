# TODO
# - localizations proper packaging
#
# Conditional build:
%bcond_without	tests		# build without tests

%define		qtver 4.3.3-3
Name:		trojita
Version:	0.3.92
Release:	0.2
Group:		X11/Applications/Mail
# Almost everything: dual-licensed under the GPLv2 or GPLv3
# (with KDE e.V. provision for relicensing)
# src/XtConnect: BSD
# src/Imap/Parser/3rdparty/kcodecs.*: LGPLv2
# Nokia imports: LGPLv2.1 or GPLv3
# src/Imap/Parser/3rdparty/rfccodecs.cpp: LGPLv2+
# src/qwwsmtpclient/: GPLv2
Summary:	Qt IMAP e-mail client
License:	(GPLv2 or GPLv3) and BSD and LGPLv2 and (LGPLv2.1 or GPLv3) and LGPLv2+ and GPLv2
URL:		http://trojita.flaska.net/
Source0:	http://downloads.sourceforge.net/trojita/%{name}-%{version}.tar.bz2
# Source0-md5:	8938d959789f0e20d724a511b265213c
BuildRequires:	QtSql-devel
BuildRequires:	QtTest-devel
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	desktop-file-utils
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-linguist >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.129
%if %{with tests}
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-xserver-Xvfb
%endif
Requires:	QtSql-sqlite3 >= %{qtver}
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# display used for testing
%define         X_display         ":98"

%description
Trojita is a Qt IMAP e-mail client which:
- Enables you to access your mail anytime, anywhere.
- Does not slow you down. If we can improve the productivity of an
  e-mail user, we better do.
- Respects open standards and facilitates modern technologies. We
  value the vendor-neutrality that IMAP provides and are committed to be
  as interoperable as possible.
- Is efficient - be it at conserving the network bandwidth, keeping
  memory use at a reasonable level or not hogging the system's CPU.
- Can be used on many platforms. One UI is not enough for everyone,
  but our IMAP core works fine on anything from desktop computers to
  cell phones and big ERP systems.
- Plays well with the rest of the ecosystem. We don't like reinventing
  wheels, but when the existing wheels quite don't fit the tracks, we're
  not afraid of making them work.

%prep
%setup -q

%build
qmake-qt4 \
	PREFIX=%{_prefix}

PATH=%{_libdir}/qt4/bin:$PATH \
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} "'$(DEFINES)'

%if %{with tests}
export DISPLAY=%{X_display}
Xvfb %{X_display} &
trap "kill $! || true" EXIT
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/%{name}/locale/trojita_common_x-test.qm

#%find_lang trojita_common --with-qt

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.*

%dir %{_datadir}/%{name}
# locales
%dir %{_datadir}/%{name}/locale
%{_datadir}/%{name}/locale/trojita_common_*.qm
