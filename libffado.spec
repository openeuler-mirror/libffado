%global _export_PLAGS \
export CFLAGS="%{optflags} -ffast-math" \
export CXXFLAGS="%{optflags} -ffast-math --std=gnu++11" \
export LDFLAGS="%{build_ldflags}"

Name:           libffado
Version:        2.4.1
Release:        8
Summary:        Free firewire audio driver library
License:        LGPLv2+ and GPLv2 and GPLv3 and GPLv3+
URL:            http://www.ffado.org/
Source0:        http://www.ffado.org/files/%{name}-%{version}.tgz
Source1:        libffado-snapshot.sh

Patch0:         0001-fix-the-AttributeError-module-posixpath-has-no-attribute-walk.patch
Patch1:         0001-fix-TypeError-must-be-str-or-None-not-bytes.patch 

BuildRequires:  alsa-lib-devel dbus-c++-devel dbus-devel python3-dbus desktop-file-utils doxygen  gcc-c++ glibmm24-devel
BuildRequires:  graphviz libappstream-glib libconfig-devel libiec61883-devel libraw1394-devel libxml++-devel pkgconfig
BuildRequires:  python3-qt5-devel python3-devel python3-enum34 python3-scons subversion
Requires:       udev dbus python3-dbus python3-qt5

Provides:       ffado = %{version}-%{release}
Obsoletes:      ffado < %{version}-%{release}

%description
The FFADO project aims to provide a universal open source solution for Linux-based FireWire-based audio device support.
It is the successor to the FreeBoB project.

%package        devel
Summary:        Free firewire audio driver library development headers
License:        GPLv2 and GPLv3
Requires:       %{name} = %{version}-%{release}

%description    devel
The libffado-devel package conatins development files to build applications for libffado.

%package        help
Summary:        Help documents for libffado

%description    help
The libffado-help package conatins manual pages for libffado.

%prep
%autosetup -p1
%ifarch riscv64
cp /usr/lib/rpm/config.guess admin/config.guess
%endif
sed -i '/Install/d' tests/{,*/}SConscript
sed -i 's|hi64-apps-ffado.png|ffado.png|' support/mixer-qt4/ffado/ffadowindow.py
sed -i 's|/usr/bin/.*python$|/usr/bin/python3|' admin/*.py doc/SConscript tests/python/*.py tests/*.py \
    support/mixer-qt4/ffado-mixer* support/mixer-qt4/SConscript support/tools/*.py support/tools/SConscript

%build
%{_export_PLAGS}
scons-3 %{?_smp_mflags} \
            ENABLE_SETBUFFERSIZE_API_VER=True ENABLE_OPTIMIZATIONS=True CUSTOM_ENV=True BUILD_DOC=user \
            PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} UDEVDIR=%{_prefix}/lib/udev/rules.d/ \
            PYPKGDIR=%{python3_sitelib}/ffado/ PYTHON_INTERPRETER=/usr/bin/python3 BUILD_TESTS=1

%install
%{_export_PLAGS}
scons-3 DESTDIR=%{buildroot} install

install -d %{buildroot}%{_datadir}/applications
desktop-file-install --dir %{buildroot}%{_datadir}/applications --add-category="Settings"  --set-icon=ffado  support/xdg/ffado.org-ffadomixer.desktop
install -d %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
ln -s ../../../../libffado/icons/hi64-apps-ffado.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/ffado.png

install -m 755 tests/ffado-test %{buildroot}%{_bindir}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%check
desktop-file-validate  %{buildroot}%{_datadir}/applications/ffado.org-ffadomixer.desktop
appstream-util validate-relax --nonet  %{buildroot}%{_datadir}/metainfo/ffado-mixer.appdata.xml

%files
%doc LICENSE.*
%dir %{_datadir}/libffado/
%{_bindir}/*
%{_libdir}/libffado.so.*
%{_libdir}/libffado/static_info.txt
%{_datadir}/libffado/*
%{_prefix}/lib/udev/rules.d/*
%{_datadir}/dbus-1/services/org.ffado.Control.service
%{_datadir}/applications/ffado.org-ffadomixer.desktop
%{_datadir}/icons/hicolor/64x64/apps/ffado.png
%{_datadir}/metainfo/ffado-mixer.appdata.xml
%{python3_sitelib}/ffado/

%files devel
%doc doc/reference/html/
%{_includedir}/libffado/
%{_libdir}/pkgconfig/libffado.pc
%{_libdir}/libffado.so

%files help
%doc AUTHORS ChangeLog README
%{_mandir}/man1/ffado-*.1*

%changelog
* Wed Feb 23 2022 YukariChiba <i@0x7f.cc> - 2.4.1-8
- Switch to use local config.guess from rpm package when building in RISC-V

* Wed Feb 23 2022 YukariChiba <i@0x7f.cc> - 2.4.1-7
- Upgrade config.guess to support RISC-V

* Tue Oct 13 2020 maminjie <maminjie1@huawei.com> - 2.4.1-6
- Rebuilt for python3

* Tue Dec 03 2019 liujing<liujing144@huawei.com> - 2.4.1-5
- Package init
