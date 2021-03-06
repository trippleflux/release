Name:           gtksourceview-sharp2
BuildRequires:  gnome-sharp2 gtk-sharp2-gapi gtksourceview-devel mono-devel monodoc-core
Requires:       gnome-sharp2
Version:        0.12
Release:        0
License:        GPL v2 or later
BuildArch:      noarch
Url:            http://www.go-mono.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         gtksourceview-sharp-2.0-%{version}.tar.bz2
Patch0:         %{name}-gnome-print.patch
Summary:        GtkSourceView bindings for Mono
Group:          Development/Libraries/Other
# Not needed with auto deps
#Requires:       gtksourceview >= 1.0 glib-sharp2 gnome-sharp2
Provides:       gtksourceview-sharp-2_0
Obsoletes:      gtksourceview-sharp-2_0
AutoReqProv:    on
# suse's gnome went from /opt/gnome to /usr, act accordingly
%define gtksourceview_prefix %(pkg-config --variable=prefix gtksourceview-1.0)
%if 0%{?suse_version}
%if %suse_version > 1100
BuildRequires:  gnome-print-sharp
Requires:       gnome-print-sharp
%endif
%if %suse_version >= 1030
BuildRequires:  -gtksourceview-devel gtksourceview18-devel
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
This package provides Mono bindings for GtkSourceView, a child of the
GTK+ text widget which implements syntax highlighting and other
features typical of a source editor.



Authors:
--------
    Martin Willemoes Hansen <mwh@sysrq.dk>
    John Luke <jluke@cfl.rr.com>
    Todd Berman <tberman@sevenl.net>
    Pawel Rozanski <tokugawa@afn.no-ip.org>
    Mike Kestner <mkestner@speakeasy.net>

%prep
%setup  -n gtksourceview-sharp-2.0-%{version} -q
%patch0

%build
autoreconf
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/gtksourceview-sharp-2.0.pc $RPM_BUILD_ROOT/usr/share/pkgconfig
rm -f $RPM_BUILD_ROOT%{gtksourceview_prefix}/share/gtksourceview-1.0/language-specs/nemerle.lang
rm -f $RPM_BUILD_ROOT%{gtksourceview_prefix}/share/gtksourceview-1.0/language-specs/vbnet.lang

%clean
rm -Rf ${DESTDIR}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README
%{_prefix}/lib/mono/gac/gtksourceview-sharp
%{_prefix}/lib/mono/gtksourceview-sharp-2.0
%{_prefix}/share/pkgconfig/gtksourceview-sharp-2.0.pc
%{_prefix}/share/gapi-2.0/gtksourceview-api.xml
%{_prefix}/lib/monodoc/sources/gtksourceview-sharp-docs*
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
