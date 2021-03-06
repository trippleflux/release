#
# spec file for package mono-core (Version 2.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

%{!?ext_man: %define ext_man .gz}
Name:           mono-core
License:        LGPL v2.1 or later
Group:          Development/Languages/Mono
Summary:        A .NET Runtime Environment
Url:            http://go-mono.org/
Version:        2.0
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        mono-%{version}.tar.bz2

ExclusiveArch: %ix86 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       mono = %{version}-%{release}
Provides:       mono-ikvm = %{version}-%{release}
Obsoletes:      mono
Obsoletes:      mono-drawing
Obsoletes:      mono-cairo
Obsoletes:      mono-xml-relaxng
Obsoletes:      mono-posix
Obsoletes:      mono-ziplib
Obsoletes:      mono-ikvm
Provides:       mono-drawing
Provides:       mono-cairo
Provides:       mono-xml-relaxng
Provides:       mono-posix
Provides:       mono-ziplib
# This version of mono has issues with the following versions of apps:
#  (not because of regressions, but because bugfixes in mono uncover bugs in the apps)
Conflicts:      helix-banshee <= 0.13.1
Conflicts:      banshee <= 0.13.1
Conflicts:      f-spot <= 0.3.5
Conflicts:      mono-addins <= 0.3
# 1.9 branch conflicts:
#  Can't do this because this rpm could be used on a distro with gtk# 2.8...
#Conflicts:	gtk-sharp2 < 2.10.3
# Require when in the buildserivce
%if 0%{?opensuse_bs}
Requires:       libgdiplus0
%endif
%if 0%{?monobuild}
Requires:       libgdiplus0
%endif
# for autobuild
%if 0%{?monobuild} == 0
%if 0%{?opensuse_bs} == 0
# suse would rather have recommends so that all sorts of graphic libs aren't 
#  pulled in when libgdiplus is installed
Recommends:     libgdiplus0
Recommends:     libgluezilla0
%endif
%endif
BuildRequires:  glib2-devel zlib-devel
#######  distro specific changes  ########
#####
#### suse options ####
%if 0%{?suse_version}
# For some reason these weren't required in 10.2 and before... ?
%if %{suse_version} >= 1030
BuildRequires:  bison
# Add valgrind support for 10.3 and above on archs that have it
%ifarch %ix86 x86_64 ppc ppc64
BuildRequires:  valgrind-devel
%endif
%endif
%if %{suse_version} >= 1020
BuildRequires:  xorg-x11-libX11
%endif
%if %{sles_version} == 10
BuildRequires:  xorg-x11-devel
%endif
%if %{suse_version} == 1010
BuildRequires:  xorg-x11-devel
%endif
%if %{sles_version} == 9
%define configure_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
BuildRequires:  XFree86-devel XFree86-libs pkgconfig
%endif
%endif
# Fedora x11
%if 0%{?fedora_version}
BuildRequires:  libX11
%endif
# rhel x11
%if 0%{?rhel_version}
BuildRequires:  libX11
%endif
#####
#######  End of distro specific changes  ########
# Why was this needed?
%ifarch s390 s390x
PreReq:         grep
%endif
# This lib only needed for ia64
%ifarch ia64
BuildRequires:  libunwind-devel
%endif
# TODO:
# This won't work until the rpm package passes .config files to mono-find-requires
#%define __find_provides env MONO_PREFIX=%{buildroot}/usr /usr/lib/rpm/find-provides
#%define __find_requires env MONO_PREFIX=%{buildroot}/usr /usr/lib/rpm/find-requires
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}/usr %{buildroot}%{_bindir}/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}/usr %{buildroot}%{_bindir}/mono-find-requires ; } | sort | uniq'

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog NEWS README
%_bindir/mono
%_libdir/libmono.so*
%_mandir/man1/mono.1%ext_man
# manpages
%_mandir/man5/mono-config.5%ext_man
%_mandir/man1/mcs.1%ext_man
%_mandir/man1/certmgr.1%ext_man
%_mandir/man1/chktrust.1%ext_man
%_mandir/man1/setreg.1%ext_man
%_mandir/man1/gacutil.1%ext_man
%_mandir/man1/sn.1%ext_man
%_mandir/man1/mozroots.1%ext_man
# wrappers
%_bindir/certmgr
%_bindir/chktrust
%_bindir/gacutil
%_bindir/gacutil2
%_bindir/gmcs
%_bindir/mono-test-install
%_bindir/mcs
%_bindir/mcs1
%_bindir/smcs
%_bindir/mozroots
%_bindir/setreg
%_bindir/sn
# exes
%_prefix/lib/mono/1.0/certmgr.exe*
%_prefix/lib/mono/1.0/chktrust.exe*
%_prefix/lib/mono/1.0/gacutil.exe*
%_prefix/lib/mono/2.0/gacutil.exe*
%_prefix/lib/mono/2.0/gmcs.exe*
%_prefix/lib/mono/1.0/mcs.exe*
%_prefix/lib/mono/1.0/mozroots.exe*
%_prefix/lib/mono/1.0/setreg.exe*
%_prefix/lib/mono/1.0/sn.exe*
%_prefix/lib/mono/gac/cscompmgd
%_prefix/lib/mono/1.0/cscompmgd.dll
%_prefix/lib/mono/2.0/cscompmgd.dll
%_prefix/lib/mono/gac/I18N.West
%_prefix/lib/mono/1.0/I18N.West.dll
%_prefix/lib/mono/2.0/I18N.West.dll
%_prefix/lib/mono/gac/I18N
%_prefix/lib/mono/1.0/I18N.dll
%_prefix/lib/mono/2.0/I18N.dll
%_prefix/lib/mono/gac/Mono.CompilerServices.SymbolWriter
%_prefix/lib/mono/1.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/2.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/gac/Mono.GetOptions
%_prefix/lib/mono/1.0/Mono.GetOptions.dll
%_prefix/lib/mono/2.0/Mono.GetOptions.dll
%_prefix/lib/mono/gac/Mono.Security
%_prefix/lib/mono/1.0/Mono.Security.dll
%_prefix/lib/mono/2.0/Mono.Security.dll
%_prefix/lib/mono/gac/System.Security
%_prefix/lib/mono/1.0/System.Security.dll
%_prefix/lib/mono/2.0/System.Security.dll
%_prefix/lib/mono/gac/System.Xml
%_prefix/lib/mono/1.0/System.Xml.dll
%_prefix/lib/mono/2.0/System.Xml.dll
%_prefix/lib/mono/2.1/System.Xml.dll
%_prefix/lib/mono/gac/System.Xml.Linq
%_prefix/lib/mono/2.0/System.Xml.Linq.dll
%_prefix/lib/mono/gac/System
%_prefix/lib/mono/1.0/System.dll
%_prefix/lib/mono/2.0/System.dll
%_prefix/lib/mono/2.1/System.dll
%_prefix/lib/mono/gac/System.Configuration
%_prefix/lib/mono/2.0/System.Configuration.dll
%_prefix/lib/mono/1.0/mscorlib.dll*
%_prefix/lib/mono/2.0/mscorlib.dll*
%_prefix/lib/mono/2.1/mscorlib.dll*
%_prefix/lib/mono/2.1/smcs.exe*
%dir %_sysconfdir/mono
%dir %_sysconfdir/mono/1.0
%dir %_sysconfdir/mono/2.0
%dir %_prefix/lib/mono
%dir %_prefix/lib/mono/1.0
%dir %_prefix/lib/mono/2.0
%dir %_prefix/lib/mono/2.1
%dir %_prefix/lib/mono/3.5
%dir %_prefix/lib/mono/gac
%config %_sysconfdir/mono/config
%config %_sysconfdir/mono/1.0/machine.config
%config %_sysconfdir/mono/2.0/machine.config
%config %_sysconfdir/mono/2.0/settings.map
%_prefix/lib/mono/gac/Mono.C5
%_prefix/lib/mono/2.0/Mono.C5.dll
# ikvm helper
%_prefix/%_lib/libikvm-native.so
%_prefix/lib/mono/gac/System.Drawing
%_prefix/lib/mono/1.0/System.Drawing.dll
%_prefix/lib/mono/2.0/System.Drawing.dll
%_libdir/libMonoPosixHelper.so*
%_prefix/lib/mono/gac/Mono.Posix
%_prefix/lib/mono/1.0/Mono.Posix.dll
%_prefix/lib/mono/2.0/Mono.Posix.dll
%_prefix/lib/mono/gac/Mono.Cairo
%_prefix/lib/mono/1.0/Mono.Cairo.dll
%_prefix/lib/mono/2.0/Mono.Cairo.dll
%_prefix/lib/mono/gac/ICSharpCode.SharpZipLib
%_prefix/lib/mono/1.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/compat-1.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/compat-2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/gac/Microsoft.VisualC
%_prefix/lib/mono/1.0/Microsoft.VisualC.dll
%_prefix/lib/mono/2.0/Microsoft.VisualC.dll
%_prefix/lib/mono/gac/Commons.Xml.Relaxng
%_prefix/lib/mono/1.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/2.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/gac/CustomMarshalers
%_prefix/lib/mono/1.0/CustomMarshalers.dll
%_prefix/lib/mono/2.0/CustomMarshalers.dll
%_prefix/lib/mono/gac/OpenSystem.C
%_prefix/lib/mono/1.0/OpenSystem.C.dll
%_prefix/lib/mono/2.0/OpenSystem.C.dll
%_prefix/lib/mono/gac/System.Core
%_prefix/lib/mono/2.0/System.Core.dll
%_prefix/lib/mono/2.1/System.Core.dll
%_prefix/lib/mono/gac/System.Net
%_prefix/lib/mono/2.1/System.Net.dll
# Not sure if autobuild allows this...
%_libdir/pkgconfig/smcs.pc

%post
/sbin/ldconfig
%ifarch s390 s390x
if grep -q "machine = 9672" /proc/cpuinfo 2>/dev/null ; then
    # anchor for rebuild on failure
    echo "mono may not work correctly on G5"
fi
%endif

%postun -p /sbin/ldconfig

%package -n mono-jscript
License:        LGPL v2.1 or later
Summary:        JScript .NET support for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-jscript
This package contains the JScript .NET compiler and language runtime.
This allows you to compile and run JScript.NET application and
assemblies.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-jscript
%defattr(-, root, root)
%_bindir/mjs
%_prefix/lib/mono/1.0/mjs.exe*
%_prefix/lib/mono/gac/Microsoft.JScript
%_prefix/lib/mono/1.0/Microsoft.JScript.dll
%_prefix/lib/mono/2.0/Microsoft.JScript.dll

%package -n mono-locale-extras
License:        LGPL v2.1 or later
Summary:        Extra locale information
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-locale-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra locale information.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-locale-extras
%defattr(-, root, root)
%_prefix/lib/mono/gac/I18N.MidEast
%_prefix/lib/mono/1.0/I18N.MidEast.dll
%_prefix/lib/mono/2.0/I18N.MidEast.dll
%_prefix/lib/mono/gac/I18N.Rare
%_prefix/lib/mono/1.0/I18N.Rare.dll
%_prefix/lib/mono/2.0/I18N.Rare.dll
%_prefix/lib/mono/gac/I18N.CJK
%_prefix/lib/mono/1.0/I18N.CJK.dll
%_prefix/lib/mono/2.0/I18N.CJK.dll
%_prefix/lib/mono/gac/I18N.Other
%_prefix/lib/mono/1.0/I18N.Other.dll
%_prefix/lib/mono/2.0/I18N.Other.dll

%package -n mono-data
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-ms-enterprise
Obsoletes:      mono-novell-directory
Obsoletes:      mono-directory
Provides:       mono-ms-enterprise
Provides:       mono-novell-directory
Provides:       mono-directory

%description -n mono-data
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data
%defattr(-, root, root)
%_prefix/lib/mono/2.0/sqlsharp.exe*
%_bindir/sqlsharp
%_mandir/man1/sqlsharp.1%ext_man
%_prefix/lib/mono/gac/System.Data
%_prefix/lib/mono/1.0/System.Data.dll
%_prefix/lib/mono/2.0/System.Data.dll
%_prefix/lib/mono/gac/System.Data.Linq
%_prefix/lib/mono/2.0/System.Data.Linq.dll
%_prefix/lib/mono/gac/Mono.Data
%_prefix/lib/mono/1.0/Mono.Data.dll
%_prefix/lib/mono/2.0/Mono.Data.dll
%_prefix/lib/mono/gac/Mono.Data.Tds
%_prefix/lib/mono/1.0/Mono.Data.Tds.dll
%_prefix/lib/mono/2.0/Mono.Data.Tds.dll
%_prefix/lib/mono/gac/Mono.Data.TdsClient
%_prefix/lib/mono/1.0/Mono.Data.TdsClient.dll
%_prefix/lib/mono/2.0/Mono.Data.TdsClient.dll
%_prefix/lib/mono/gac/System.EnterpriseServices
%_prefix/lib/mono/1.0/System.EnterpriseServices.dll
%_prefix/lib/mono/2.0/System.EnterpriseServices.dll
%_prefix/lib/mono/gac/Novell.Directory.Ldap
%_prefix/lib/mono/1.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/2.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/gac/System.DirectoryServices
%_prefix/lib/mono/1.0/System.DirectoryServices.dll
%_prefix/lib/mono/2.0/System.DirectoryServices.dll
%_prefix/lib/mono/gac/System.Transactions
%_prefix/lib/mono/2.0/System.Transactions.dll
%_prefix/lib/mono/gac/System.Data.DataSetExtensions
%_prefix/lib/mono/2.0/System.Data.DataSetExtensions.dll

%package -n mono-winforms
License:        LGPL v2.1 or later
Summary:        Mono's Windows Forms implementation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Provides:       mono-window-forms
Obsoletes:      mono-window-forms

%description -n mono-winforms
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's Windows Forms implementation.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-winforms
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.Windows.Forms
%_prefix/lib/mono/1.0/System.Windows.Forms.dll
%_prefix/lib/mono/2.0/System.Windows.Forms.dll
%_prefix/lib/mono/gac/Accessibility
%_prefix/lib/mono/1.0/Accessibility.dll
%_prefix/lib/mono/2.0/Accessibility.dll
%_prefix/lib/mono/gac/System.Design
%_prefix/lib/mono/1.0/System.Design.dll
%_prefix/lib/mono/2.0/System.Design.dll
%_prefix/lib/mono/gac/System.Drawing.Design
%_prefix/lib/mono/1.0/System.Drawing.Design.dll
%_prefix/lib/mono/2.0/System.Drawing.Design.dll
# TODO: Post 1.2.5:
%_prefix/lib/mono/1.0/Mono.WebBrowser.dll
%_prefix/lib/mono/2.0/Mono.WebBrowser.dll
%_prefix/lib/mono/gac/Mono.WebBrowser

%package -n ibm-data-db2
License:        LGPL v2.1 or later
Summary:        Database connectivity for DB2
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n ibm-data-db2
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for DB2.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n ibm-data-db2
%defattr(-, root, root)
%_prefix/lib/mono/gac/IBM.Data.DB2
%_prefix/lib/mono/1.0/IBM.Data.DB2.dll
%_prefix/lib/mono/2.0/IBM.Data.DB2.dll

%package -n mono-extras
License:        LGPL v2.1 or later
Summary:        Extra packages
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-ms-extras
Provides:       mono-ms-extras

%description -n mono-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra packages.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-extras
%defattr(-, root, root)
%_mandir/man1/mono-service.1%ext_man
%_bindir/mono-service
%_bindir/mono-service2
# These are errors because they should be symlinks, but they are copies, so rpmlint detects duplicate files
%_prefix/lib/mono/gac/mono-service
%_prefix/lib/mono/1.0/mono-service.exe*
%_prefix/lib/mono/2.0/mono-service.exe*
%_prefix/lib/mono/gac/System.Management
%_prefix/lib/mono/1.0/System.Management.dll
%_prefix/lib/mono/2.0/System.Management.dll
%_prefix/lib/mono/gac/System.Messaging
%_prefix/lib/mono/1.0/System.Messaging.dll
%_prefix/lib/mono/2.0/System.Messaging.dll
%_prefix/lib/mono/gac/System.ServiceProcess
%_prefix/lib/mono/1.0/System.ServiceProcess.dll
%_prefix/lib/mono/2.0/System.ServiceProcess.dll
%_prefix/lib/mono/gac/System.Configuration.Install
%_prefix/lib/mono/1.0/System.Configuration.Install.dll
%_prefix/lib/mono/2.0/System.Configuration.Install.dll
%_prefix/lib/mono/gac/Microsoft.Vsa
%_prefix/lib/mono/1.0/Microsoft.Vsa.dll
%_prefix/lib/mono/2.0/Microsoft.Vsa.dll

%package -n mono-data-sqlite
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release
# TODO: Disable this, until a better solution is found
#Requires:       sqlite2

%description -n mono-data-sqlite
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-sqlite
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Data.SqliteClient
%_prefix/lib/mono/1.0/Mono.Data.SqliteClient.dll
%_prefix/lib/mono/2.0/Mono.Data.SqliteClient.dll
%_prefix/lib/mono/gac/Mono.Data.Sqlite
%_prefix/lib/mono/1.0/Mono.Data.Sqlite.dll
%_prefix/lib/mono/2.0/Mono.Data.Sqlite.dll

%package -n mono-data-sybase
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-sybase
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-sybase
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Data.SybaseClient
%_prefix/lib/mono/1.0/Mono.Data.SybaseClient.dll
%_prefix/lib/mono/2.0/Mono.Data.SybaseClient.dll

%package -n mono-wcf
Summary:        Mono implementation of WCF, Windows Communication Foundation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-wcf
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of WCF, Windows Communication Foundation



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>


%files -n mono-wcf
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.IdentityModel
%_prefix/lib/mono/2.0/System.IdentityModel.dll
%_prefix/lib/mono/gac/System.IdentityModel.Selectors
%_prefix/lib/mono/2.0/System.IdentityModel.Selectors.dll
%_prefix/lib/mono/gac/System.Runtime.Serialization
%_prefix/lib/mono/2.0/System.Runtime.Serialization.dll
%_prefix/lib/mono/gac/System.ServiceModel
%_prefix/lib/mono/2.0/System.ServiceModel.dll
%_prefix/lib/mono/gac/System.ServiceModel.Web
%_prefix/lib/mono/2.0/System.ServiceModel.Web.dll
%_libdir/pkgconfig/wcf.pc

%package -n mono-web
License:        LGPL v2.1 or later
Summary:        Mono implementation of ASP.NET, Remoting and Web Services
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-web-forms
Obsoletes:      mono-web-services
Obsoletes:      mono-remoting
Provides:       mono-web-forms
Provides:       mono-web-services
Provides:       mono-remoting

%description -n mono-web
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET, Remoting and Web Services.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-web
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Http
%_prefix/lib/mono/1.0/Mono.Http.dll
%_prefix/lib/mono/2.0/Mono.Http.dll
%_prefix/lib/mono/gac/Mono.Web
%_prefix/lib/mono/2.0/Mono.Web.dll
%_prefix/lib/mono/gac/System.Runtime.Remoting
%_prefix/lib/mono/1.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/2.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/gac/System.Web
%_prefix/lib/mono/1.0/System.Web.dll
%_prefix/lib/mono/2.0/System.Web.dll
%_prefix/lib/mono/gac/System.Runtime.Serialization.Formatters.Soap
%_prefix/lib/mono/1.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/2.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/gac/System.Web.Services
%_prefix/lib/mono/1.0/System.Web.Services.dll
%_prefix/lib/mono/2.0/System.Web.Services.dll
%_prefix/lib/mono/gac/System.Web.Extensions
%_prefix/lib/mono/2.0/System.Web.Extensions.dll
%_prefix/lib/mono/3.5/System.Web.Extensions.dll
%_prefix/lib/mono/gac/System.Web.Extensions.Design
%_prefix/lib/mono/2.0/System.Web.Extensions.Design.dll
%_prefix/lib/mono/3.5/System.Web.Extensions.Design.dll
# exes
%_prefix/lib/mono/1.0/disco.exe*
%_prefix/lib/mono/1.0/soapsuds.exe*
%_prefix/lib/mono/1.0/wsdl.exe*
%_prefix/lib/mono/2.0/wsdl.exe*
%_prefix/lib/mono/1.0/xsd.exe*
%_prefix/lib/mono/2.0/xsd.exe*
%_prefix/lib/mono/2.0/mconfig.exe*
# shell wrappers
%_bindir/disco
%_bindir/mconfig
%_bindir/soapsuds
%_bindir/wsdl
%_bindir/wsdl1
%_bindir/wsdl2
%_bindir/xsd
%_bindir/xsd2
# man pages
%_mandir/man1/disco.1%ext_man
%_mandir/man1/soapsuds.1%ext_man
%_mandir/man1/wsdl.1%ext_man
%_mandir/man1/xsd.1%ext_man
%_mandir/man1/mconfig.1%ext_man
%config %_sysconfdir/mono/browscap.ini
%dir %_sysconfdir/mono/mconfig
%config %_sysconfdir/mono/mconfig/config.xml
%config %_sysconfdir/mono/1.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/2.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/2.0/web.config
%config %_sysconfdir/mono/2.0/Browsers

%package -n mono-data-oracle
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-oracle
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-oracle
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.Data.OracleClient
%_prefix/lib/mono/1.0/System.Data.OracleClient.dll
%_prefix/lib/mono/2.0/System.Data.OracleClient.dll

%package -n mono-data-postgresql
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-postgresql
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-postgresql
%defattr(-, root, root)
%_prefix/lib/mono/gac/Npgsql
%_prefix/lib/mono/1.0/Npgsql.dll
%_prefix/lib/mono/2.0/Npgsql.dll

%package -n bytefx-data-mysql
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n bytefx-data-mysql
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n bytefx-data-mysql
%defattr(-, root, root)
%_prefix/lib/mono/gac/ByteFX.Data
%_prefix/lib/mono/1.0/ByteFX.Data.dll
%_prefix/lib/mono/2.0/ByteFX.Data.dll

%package -n mono-nunit
License:        LGPL v2.1 or later
Summary:        NUnit Testing Framework
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%package -n mono-data-firebird
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-firebird
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



%files -n mono-data-firebird
%defattr(-, root, root)
%_prefix/lib/mono/gac/FirebirdSql.Data.Firebird
%_prefix/lib/mono/1.0/FirebirdSql.Data.Firebird.dll

%description -n mono-nunit
NUnit is a unit-testing framework for all .Net languages.  Initially
ported from JUnit, the current release, version 2.2,  is the fourth
major release of this  Unit based unit testing tool for Microsoft .NET.
It is written entirely in C# and  has been completely redesigned to
take advantage of many .NET language		 features, for example
custom attributes and other reflection related capabilities. NUnit
brings xUnit to all .NET languages.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-nunit
%defattr(-, root, root)
%_prefix/bin/nunit-console
%_prefix/bin/nunit-console2
%_prefix/lib/mono/1.0/nunit-console.exe*
%_prefix/lib/mono/2.0/nunit-console.exe*
%_prefix/lib/mono/gac/nunit.util
%_prefix/lib/mono/1.0/nunit.util.dll
%_prefix/lib/mono/2.0/nunit.util.dll
%_prefix/lib/mono/gac/nunit.core
%_prefix/lib/mono/1.0/nunit.core.dll
%_prefix/lib/mono/2.0/nunit.core.dll
%_prefix/lib/mono/gac/nunit.framework
%_prefix/lib/mono/1.0/nunit.framework.dll
%_prefix/lib/mono/2.0/nunit.framework.dll
%_prefix/lib/mono/gac/nunit.mocks
%_prefix/lib/mono/1.0/nunit.mocks.dll
%_prefix/lib/mono/2.0/nunit.mocks.dll
%_libdir/pkgconfig/mono-nunit.pc

%package -n mono-devel
License:        LGPL v2.1 or later
Summary:        Mono development tools
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       glib2-devel

%description -n mono-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. This package contains compilers and
other tools needed to develop .NET applications.

Mono development tools.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%post -n mono-devel
/sbin/ldconfig
if [ ! -d /opt/gnome ]; then
sed -i 's:/opt/gnome:/usr:g' %_libdir/libmono.la
fi

%postun -n mono-devel -p /sbin/ldconfig

%files -n mono-devel
%defattr(-, root, root)
# libs
%_libdir/libmono.a
%verify(not size md5 mtime) %_libdir/libmono.la
# exes
%_prefix/lib/mono/1.0/makecert.exe*
%_prefix/lib/mono/1.0/mono-api-info.exe*
%_prefix/lib/mono/2.0/mono-api-info.exe*
%_prefix/lib/mono/1.0/mono-api-diff.exe*
%_prefix/lib/mono/1.0/al.exe*
%_prefix/lib/mono/2.0/al.exe*
%_prefix/lib/mono/1.0/caspol.exe*
%_prefix/lib/mono/1.0/cert2spc.exe*
%_prefix/lib/mono/1.0/dtd2xsd.exe*
%_prefix/lib/mono/1.0/genxs.exe*
%_prefix/lib/mono/2.0/httpcfg.exe*
%_prefix/lib/mono/1.0/ictool.exe*
%_prefix/lib/mono/1.0/ilasm.exe*
%_prefix/lib/mono/2.0/ilasm.exe*
%_prefix/lib/mono/1.0/installvst.exe*
%_prefix/lib/mono/1.0/installutil.exe*
%_prefix/lib/mono/2.0/installutil.exe*
%_prefix/lib/mono/1.0/mkbundle.exe*
%_prefix/lib/mono/2.0/mkbundle.exe*
%_prefix/lib/mono/1.0/monop.exe*
%_prefix/lib/mono/2.0/monop.exe*
%_prefix/lib/mono/1.0/permview.exe*
%_prefix/lib/mono/1.0/resgen.exe*
%_prefix/lib/mono/2.0/resgen.exe*
%_prefix/lib/mono/1.0/secutil.exe*
%_prefix/lib/mono/2.0/sgen.exe*
%_prefix/lib/mono/1.0/signcode.exe*
%_prefix/lib/mono/1.0/prj2make.exe*
%_prefix/lib/mono/1.0/macpack.exe*
%_prefix/lib/mono/1.0/mono-shlib-cop.exe*
%_prefix/lib/mono/1.0/dtd2rng.exe*
%_prefix/lib/mono/1.0/mono-xmltool.exe*
# xbuild related files
%_prefix/lib/mono/2.0/xbuild.exe*
%_prefix/lib/mono/2.0/Microsoft.Build.xsd
%_prefix/lib/mono/2.0/Microsoft.Common.tasks
%_prefix/lib/mono/2.0/Microsoft.Common.targets
%_prefix/lib/mono/2.0/Microsoft.CSharp.targets
%_prefix/lib/mono/2.0/Microsoft.VisualBasic.targets
%_prefix/lib/mono/2.0/MSBuild
%_prefix/lib/mono/2.0/xbuild.rsp
# man pages
%_mandir/man1/cert2spc.1%ext_man
%_mandir/man1/dtd2xsd.1%ext_man
%_mandir/man1/genxs.1%ext_man
%_mandir/man1/httpcfg.1%ext_man
%_mandir/man1/ilasm.1%ext_man
%_mandir/man1/macpack.1%ext_man
%_mandir/man1/makecert.1%ext_man
%_mandir/man1/mkbundle.1%ext_man
%_mandir/man1/monodis.1%ext_man
%_mandir/man1/monop.1%ext_man
%_mandir/man1/mono-shlib-cop.1%ext_man
%_mandir/man1/permview.1%ext_man
%_mandir/man1/prj2make.1%ext_man
%_mandir/man1/secutil.1%ext_man
%_mandir/man1/sgen.1%ext_man
%_mandir/man1/signcode.1%ext_man
%_mandir/man1/al.1%ext_man
%_mandir/man1/mono-xmltool.1%ext_man
%_mandir/man1/resgen.1%ext_man
# Shell wrappers
%_bindir/al
%_bindir/al1
%_bindir/al2
%_bindir/caspol
%_bindir/cert2spc
%_bindir/dtd2xsd
%_bindir/dtd2rng
%_bindir/genxs
%_bindir/genxs1
%_bindir/genxs2
%_bindir/httpcfg
%_bindir/ilasm
%_bindir/ilasm1
%_bindir/ilasm2
%_bindir/installvst
%_bindir/macpack
%_bindir/makecert
%_bindir/mkbundle
%_bindir/mkbundle1
%_bindir/mkbundle2
%_bindir/monodis
%_bindir/monolinker
%_bindir/monop
%_bindir/monop1
%_bindir/monop2
%_bindir/mono-api-diff
%_bindir/mono-api-info
%_bindir/mono-api-info1
%_bindir/mono-api-info2
%_bindir/mono-find-provides
%_bindir/mono-find-requires
%_bindir/mono-shlib-cop
%_bindir/mono-xmltool
%_bindir/pedump
%_bindir/permview
%_bindir/prj2make
%_bindir/resgen
%_bindir/resgen1
%_bindir/resgen2
%_bindir/secutil
%_bindir/sgen
%_bindir/signcode
%_bindir/xbuild
%_mandir/man1/monolinker.1%ext_man
%_prefix/lib/mono/gac/PEAPI
%_prefix/lib/mono/1.0/PEAPI.dll
%_prefix/lib/mono/1.0/monolinker.*
%_prefix/lib/mono/2.0/PEAPI.dll
%_prefix/lib/mono/gac/Microsoft.Build.Tasks
%_prefix/lib/mono/2.0/Microsoft.Build.Tasks.dll
%_prefix/lib/mono/gac/Microsoft.Build.Framework
%_prefix/lib/mono/2.0/Microsoft.Build.Framework.dll
%_prefix/lib/mono/gac/Microsoft.Build.Utilities
%_prefix/lib/mono/2.0/Microsoft.Build.Utilities.dll
%_prefix/lib/mono/gac/Microsoft.Build.Engine
%_prefix/lib/mono/2.0/Microsoft.Build.Engine.dll
%_prefix/lib/mono/gac/Mono.Cecil
%_prefix/lib/mono/gac/Mono.Cecil.Mdb
%_bindir/monograph
%_prefix/include/mono-1.0
%_libdir/libmono-profiler-cov.*
%_libdir/libmono-profiler-aot.*
%_libdir/libmono-profiler-logging.*
%_libdir/pkgconfig/mono.pc
%_libdir/pkgconfig/dotnet.pc
%_libdir/pkgconfig/dotnet35.pc
%_libdir/pkgconfig/mono-cairo.pc
%_libdir/pkgconfig/cecil.pc
%_mandir/man1/monoburg.*
%_prefix/share/mono-1.0/mono/cil/cil-opcodes.xml
# dirs
%dir %_prefix/share/mono-1.0
%dir %_prefix/share/mono-1.0/mono
%dir %_prefix/share/mono-1.0/mono/cil
# Reminder: when removing man pages in this list, they are not 
#  yet gzipped

%package -n mono-complete
License:        LGPL v2.1 or later
Summary:        A .NET Runtime Environment
Group:          Development/Languages/Mono
Requires:       bytefx-data-mysql = %version-%release
Requires:       ibm-data-db2 = %version-%release
Requires:       mono-core = %version-%release
Requires:       mono-data = %version-%release
Requires:       mono-data-firebird = %version-%release
Requires:       mono-data-oracle = %version-%release
Requires:       mono-data-postgresql = %version-%release
Requires:       mono-data-sqlite = %version-%release
Requires:       mono-data-sybase = %version-%release
Requires:       mono-devel = %version-%release
Requires:       mono-extras = %version-%release
Requires:       mono-jscript = %version-%release
Requires:       mono-locale-extras = %version-%release
Requires:       mono-nunit = %version-%release
Requires:       mono-web = %version-%release
Requires:       mono-wcf = %version-%release
Requires:       mono-winforms = %version-%release

%description -n mono-complete
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-complete
%defattr(-, root, root)
# Directories
# Put dir files here so we don't have an empty package
%dir %_prefix/lib/mono/compat-1.0
%dir %_prefix/lib/mono/compat-2.0

%debug_package
%prep
%setup -q -n mono-%{version}

%build
# These are only needed if there are patches to the runtime
#rm -f libgc/libtool.m4
#autoreconf --force --install
#autoreconf --force --install libgc
export CFLAGS=" $RPM_OPT_FLAGS -DKDE_ASSEMBLIES='\"/opt/kde3/%{_lib}\"' -fno-strict-aliasing"
# distro specific configure options
%{?configure_options}
%configure \
  --with-jit=yes \
  --with-ikvm=yes \
  --with-sigaltstack=no \
  --with-moonlight=yes
make

%install
make DESTDIR="$RPM_BUILD_ROOT" install

# Remove unused files
rm $RPM_BUILD_ROOT%_libdir/libMonoPosixHelper.a
rm $RPM_BUILD_ROOT%_libdir/libMonoPosixHelper.la
rm -f $RPM_BUILD_ROOT%_libdir/libikvm-native.a
rm -f $RPM_BUILD_ROOT%_libdir/libikvm-native.la
rm -fr $RPM_BUILD_ROOT%_prefix/lib/mono/gac/Mono.Security.Win32/[12]*
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/Mono.Security.Win32.dll
rm $RPM_BUILD_ROOT%_prefix/lib/mono/2.0/Mono.Security.Win32.dll
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.DGUX386
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.Mac
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.MacOSX
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.OS2
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.amiga
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.arm.cross
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.autoconf
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.changes
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.contributors
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.cords
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.darwin
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.dj
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.environment
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.ews4800
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.hp
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.linux
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.macros
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.rs6000
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.sgi
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.solaris2
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.uts
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.win32
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/barrett_diagram
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/debugging.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gc.man
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gcdescr.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gcinterface.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/leak.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/scale.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/simple_example.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/tree.html
rm $RPM_BUILD_ROOT%_mandir/man1/cilc.1
rm $RPM_BUILD_ROOT%_mandir/man1/monostyle.1
rm $RPM_BUILD_ROOT%_mandir/man1/oldmono.1
rm $RPM_BUILD_ROOT%_mandir/man1/mint.1
# Things we don't ship.
# cilc
rm $RPM_BUILD_ROOT%_bindir/cilc
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/cilc*
# jay
rm $RPM_BUILD_ROOT%_bindir/jay
rm -R $RPM_BUILD_ROOT%_datadir/jay
rm $RPM_BUILD_ROOT%_mandir/man1/jay.1
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/CorCompare.exe
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/browsercaps-updater.exe*
# New files to delete in 1.1.9.2
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.a
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.la
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.so
# 1.1.17 updates:
# This file moved to mono-basic
rm -f $RPM_BUILD_ROOT%_bindir/mbas
# 1.2.4 changes
rm -f $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/culevel.exe*
# Post 1.2.5
rm -f $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/transform.exe
# brp-compress doesn't search _mandir
# so we cheat it
ln -s . %buildroot%_prefix/usr
RPM_BUILD_ROOT=%buildroot%_prefix /usr/lib/rpm/brp-compress
rm %buildroot%_prefix/usr

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
