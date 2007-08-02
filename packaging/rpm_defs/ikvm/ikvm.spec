
# norootforbuild

Name:           ikvm
BuildRequires:  mono-core mono-devel unzip
Version:        0.34.0.2
Release:        1
License:        BSD License and BSD-like
BuildArch:      noarch
URL:            http://www.ikvm.net
Source0:        ikvmbin-%{version}.zip
Summary:        A JVM Based on the Mono Runtime
Group:          Development/Tools/Other
Requires:       mono-ikvm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

####  fedora  ####
%if 0%{?fedora_version}
# All fedora distros (5 and 6) have the same names, requirements
# Needed to generate wrapper
BuildRequires: which
%endif
#################


%description
This package provides IKVM.NET, an open source Java compatibility layer
for Mono, which includes a Virtual Machine, a bytecode compiler, and
various class libraries for Java, as well as tools for Java and Mono
interoperability.



Authors:
--------
    Jeroen Frijters <jfrijters@users.sourceforge.net>

%prep
%setup -q
# For some reason this file is outside the source dir...
cp ../LICENSE .

%build
true

%install
# Create dirs
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/ikvm
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/pkgconfig
#Install binaries
find bin . -name "*\.dll" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
find bin . -name "*\.exe" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
# Generate wrapper scripts
for f in `find bin . -name "*\.exe"` ; do
        script_name=${RPM_BUILD_ROOT}/usr/bin/`basename $f .exe`
        cat <<EOF > $script_name
#!/bin/sh
exec `which mono` /usr/lib/ikvm/`basename $f` "\$@"
EOF
        chmod 755 $script_name
done
%define prot_name Name
%define prot_version Version
# Generate .pc file
cat <<EOF > ${RPM_BUILD_ROOT}/usr/lib/pkgconfig/ikvm.pc
prefix=/usr
exec_prefix=\${prefix}
libdir=\${prefix}/lib

%prot_name: IKVM.NET
Description: An implementation of Java for Mono and the Microsoft .NET Framework.

%prot_version: %{version}
Libs: -r:\${libdir}/ikvm/IKVM.Runtime.dll -r:\${libdir}/ikvm/IKVM.GNU.Classpath.dll
EOF
# Move .pc to share instead of lib
mkdir -p ${RPM_BUILD_ROOT}/usr/share/pkgconfig
mv ${RPM_BUILD_ROOT}/usr/lib/pkgconfig/ikvm.pc ${RPM_BUILD_ROOT}/usr/share/pkgconfig

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root)
%doc LICENSE
/usr/bin/*
/usr/lib/ikvm
/usr/share/pkgconfig/ikvm.pc

# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog