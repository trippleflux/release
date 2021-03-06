import re

ignoresource = re.compile("\.(no)?src\.rpm$")
matchrpm = re.compile("\.rpm$")

valid_arch = {
	'ia64':		'ia64 noarch',
	'i386':		'i686 i586 i386 noarch',
	'i586':		'i686 i586 i386 noarch',
        'ppc':		'ppc noarch',
	's390':		's390 noarch',
	's390x':	's390x s390 noarch',
	'x86_64':	'x86_64 i686 i586 i386 noarch',
}

# top level keys represent host machine, sub level keys are jail targets
#  bottom value is the command to emulate the jail target
bi_arch_switch = {
	'x86_64':
		{
			'i386': 'linux32',
			'i586': 'linux32',
		},
	's390x':
		{
			's390': 's390',
		},
}

required_rpms = {
	#ftp://ftp.novell.com/pub/ximian/redcarpet2/sles-9-ia64/
	'sles-9': """
		XFree86-devel
		XFree86-libs
		aaa_base
		aaa_skel
		apache2
		apache2-devel
		apache2-prefork
		autoconf
		automake
		bison
		cpio
		esound-devel
		expat
		file
		fontconfig
		fontconfig-devel
		freetype2
		freetype2-devel
		gcc
		gdb
		glib2
		glib2-devel
		glibc-devel
		gnome-vfs2
		gtk2-devel
		gtksourceview-devel
		iputils
		kbd
		libapr0
		libart_lgpl-devel
		libbonoboui
		libexif
		libglade2-devel
		libgnome
		libgnomecanvas-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui
		libgnomeui-devel
		libgsf-devel
		libjpeg
		libpng
		libpng-devel
		librsvg-devel
		libtiff
		libtool
		libungif
		libxml2-devel
		libxslt-devel
		m4
		make
		mktemp
		ncurses-devel
		netcfg
		pango-devel
		patch
		perl-XML-Parser
		pkgconfig
		popt-devel
		procps
		pwdutils
		rug
		sles-release
		sudo
		tar
		termcap
		timezone
		unzip
		util-linux
		vim
		vte
		vte-devel
		wget
		yast2
		yast2-ncurses
		yast2-ncurses
		yast2-packager
		zlib-devel
	""",

	'sles-10': """
		ImageMagick-Magick++-devel
		aaa_base
		apache2-devel
		apache2-prefork
		autoconf
		automake
		avahi
		dbus-1-devel
		dos2unix
		esound-devel
		file
		freetype2-devel
		gcc
		gcc-c++
		gecko-sdk
		giflib-devel
		glib2-devel
		glibc-locale
		gnome-keyring-devel
		gnome-panel-nld-devel
		gstreamer010-devel
		gstreamer010-plugins-base-devel
		gtk2-devel
		gtkhtml2-devel
		gtksourceview
		gtksourceview-devel
		intltool
		iputils
		libart_lgpl-devel
		libglade2-devel
		libgnomecanvas-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui-devel
		libgsf-devel
		libjpeg-devel
		libpng-devel
		librsvg
		librsvg-devel
		libtiff-devel
		libtool
		libxslt-devel
		make
		makedev
		mozilla-nspr-devel
		mozilla-xulrunner
		mDNSResponder-devel
		ncurses-devel
		patch
		perl-XML-LibXML
		perl-XML-LibXML-Common
		perl-XML-NamespaceSupport
		perl-XML-Parser
		perl-XML-SAX
		pkgconfig
		popt-devel
		procps
		pwdutils
		smart
		sqlite
		sudo
		sysvinit
		tar
		unzip
		update-desktop-files
		util-linux
		vim
		vte-devel
		wget
		xorg-x11
		xorg-x11-devel
		xorg-x11-Xnest
		xorg-x11-Xvfb
		yast2
		yast2-ncurses
		zip
		zlib-devel
	""",

	'suse-101': """
		ImageMagick-Magick++-devel
		aaa_base
		apache2-devel
		apache2-prefork
		autoconf
		automake
		avahi
		dbus-1-devel
		dos2unix
		esound-devel
		file
		freetype2-devel
		gcc
		giflib-devel
		glib2-devel
		glibc-locale
		gnome-keyring-devel
		gnome-panel-devel
		gstreamer010-devel
		gstreamer010-plugins-base-devel
		gtk2-devel
		gtkhtml2-devel
		gtksourceview
		gtksourceview-devel
		iputils
		libart_lgpl-devel
		libglade2-devel
		libgnomecanvas-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui-devel
		libgsf-devel
		libjpeg-devel
		libpng-devel
		librsvg
		librsvg-devel
		libtiff-devel
		libtool
		libxslt-devel
		make
		makedev
		mDNSResponder-devel
		ncurses-devel
		patch
		perl-XML-LibXML
		perl-XML-LibXML-Common
		perl-XML-NamespaceSupport
		perl-XML-Parser
		perl-XML-SAX
		pkgconfig
		popt-devel
		procps
		pwdutils
		smart
		sqlite2
		sudo
		sysvinit
		tar
		unzip
		util-linux
		vim
		vte-devel
		wget
		xorg-x11
		xorg-x11-devel
		xorg-x11-Xnest
		xorg-x11-Xvfb
		yast2
		yast2-ncurses
		zip
		zlib-devel
	""",

	'suse-102': """
		aaa_base
		apache2-devel
		apache2-prefork
		autoconf
		automake
		bc
		bison
		esound-devel
		file
		freetype2-devel
		gcc
		gcc-c++
		giflib-devel
		glib2-devel
		glibc-locale
		gnome-keyring-devel
		gnome-panel-devel
		gstreamer010-devel
		gstreamer010-plugins-base-devel
		gtk2-devel
		gtkhtml2-devel
		gtksourceview-devel
		intltool
		iputils
		libart_lgpl-devel
		libglade2-devel
		libgnomecanvas-devel
		libgnomedb-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui-devel
		libgsf-devel
		libjpeg-devel
		libpng-devel
		librsvg
		librsvg-devel
		libtiff-devel
		libtool
		libxslt-devel
		make
		makedev
		mozilla-nspr-devel
		mozilla-xulrunner181-devel
		patch
		perl-XML-LibXML
		perl-XML-LibXML-Common
		perl-XML-NamespaceSupport
		perl-XML-Parser
		perl-XML-SAX
		pkgconfig
		popt-devel
		procps
		pwdutils
		rsync
		sqlite2
		subversion
		openssh
		sudo
		sysvinit
		tar
		update-desktop-files
		unzip
		util-linux
		vim
		vte-devel
		wget
		xorg-x11-devel
		yast2
		yast2-ncurses
		zip
		zlib-devel
		zypper
	""",

	'suse-103': """
		aaa_base
		apache2-devel
		apache2-prefork
		autoconf
		automake
		bc
		bison
		esound-devel
		file
		freetype2-devel
		gcc
		gcc-c++
		giflib-devel
		glib2-devel
		glibc-locale
		gnome-keyring-devel
		gnome-panel-devel
		gstreamer010-devel
		gstreamer010-plugins-base-devel
		gtk2-devel
		gtkhtml2-devel
		gtksourceview-devel
		gtksourceview18-devel
		intltool
		iputils
		libart_lgpl-devel
		libexif-devel
		libglade2-devel
		libgnomedb-devel
		libgnomecanvas-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui-devel
		libgsf-devel
		libjpeg-devel
		libpng-devel
		librsvg
		librsvg-devel
		libtiff-devel
		libtool
		libwnck-devel
		libxslt-devel
		make
		makedev
		mozilla-nspr-devel
		mozilla-xulrunner181-devel
		nautilus-cd-burner-devel
		patch
		perl-XML-LibXML
		perl-XML-LibXML-Common
		perl-XML-NamespaceSupport
		perl-XML-Parser
		perl-XML-SAX
		pkg-config
		popt-devel
		procps
		pwdutils
		rsync
		sqlite2
		subversion
		openssh
		sudo
		sysvinit
		tar
		update-desktop-files
		unzip
		util-linux
		vim
		vte-devel
		wget
		xorg-x11-devel
		yast2
		yast2-ncurses
		zip
		zlib-devel
		zypper
	""",
	'suse-110': """
		aaa_base
		apache2-devel
		apache2-prefork
		autoconf
		automake
		bc
		bison
		esound-devel
		file
		freetype2-devel
		gcc
		gcc-c++
		giflib-devel
		glib2-devel
		glibc-locale
		gnome-keyring-devel
		gnome-panel-devel
		gstreamer010-devel
		gstreamer010-plugins-base-devel
		gtk2-devel
		gtkhtml2-devel
		gtksourceview-devel
		gtksourceview18-devel
		intltool
		iputils
		libart_lgpl-devel
		libexif-devel
		libglade2-devel
		libgnomedb-devel
		libgnomecanvas-devel
		libgnomeprint
		libgnomeprint-devel
		libgnomeprintui
		libgnomeprintui-devel
		libgnomeui-devel
		libgsf-devel
		libjpeg-devel
		libpng-devel
		librsvg
		librsvg-devel
		libtiff-devel
		libtool
		libwnck-devel
		libxslt-devel
		make
		makedev
		mozilla-nspr-devel
		mozilla-xulrunner181-devel
		nautilus-cd-burner-devel
		patch
		perl-XML-LibXML
		perl-XML-LibXML-Common
		perl-XML-NamespaceSupport
		perl-XML-Parser
		perl-XML-SAX
		pkg-config
		popt-devel
		procps
		pwdutils
		rsync
		sqlite2
		subversion
		openssh
		sudo
		sysvinit
		tar
		update-desktop-files
		unzip
		util-linux
		vim
		vte-devel
		wget
		xorg-x11-devel
		yast2
		yast2-ncurses
		zip
		zlib-devel
		zypper
	""",

	'fedora-5': """
		autoconf
		automake
		bzip2
		coreutils
		fontconfig-devel
		freetype-devel
		gcc
		gcc-c++
		giflib-devel
		glib2-devel
		gnome-panel-devel
		gtk2-devel
		gtkhtml3-devel
		httpd-devel
		libX11-devel
		libXrender-devel
		libart_lgpl-devel
		libexif-devel
		libglade2-devel
		libgnomecanvas-devel
		libgnomeprintui22-devel
		libgnomeui-devel
		libjpeg-devel
		libpng-devel
		librsvg2-devel
		libtiff-devel
		libtool
		libXt-devel
		libxml2-devel
		make
		openssh-clients
		pango-devel
		perl-XML-Parser
		perl-XML-Simple
		pkgconfig
		rpm-build
		sqlite-devel
		sudo
		tcl
		vim-enhanced
		vte-devel
		which
		yum
		zlib-devel
	""",

	'rhel-4': """
		autoconf
		automake
		bison
		bzip2
		coreutils
		diffutils
		file
		flex
		gcc
		gcc-c++
		gettext
		make
		ncurses-devel
		openssh-clients
		patch
		pkgconfig
		screen
		subversion
		sudo
		texinfo
		vim-enhanced
		which
		yum
		zlib-devel
	""",

}

environment = {
	'redhat-9':	"LD_ASSUME_KERNEL=2.2.5",
}


# Other various/optional post jail settings:
settings = {
        'nameservers':  '137.65.1.3 137.65.1.4 130.57.22.5',
        'users':        'builder',
}

post_install_notes = {

	'suse-101':	"""# Create some devices:
mknod -m 666 /dev/null c 1 3
mknod -m 666 /dev/zero c 1 5 
mknod -m 666 /dev/random  c  1 8
mknod -m 644 /dev/urandom c  1 9
""",
	'suse-102':	"""# Create some devices:
mknod -m 666 /dev/null c 1 3
mknod -m 666 /dev/zero c 1 5 
mknod -m 666 /dev/random  c  1 8
mknod -m 644 /dev/urandom c  1 9

	Also, had to comment out my_test_for_space in SuSEconfig script
""",
	'suse-103':	"""# vi is messed up:
rm /bin/vim
ln -s /bin/vim-normal /bin/vim
""",
	'fedora-4':	"""Disable gpg keys and set gpgcheck to 0 in /etc/yum.repos.d/*
MAKEDEV in /dev for random, urandom and null, touch /etc/fstab""",

	'fedora-5':	"""# MAKEDEV in /dev for random, urandom and null, Add /proc to /etc/fstab""",
	'sles-9-ia64':	"""Had to copy /etc/sysconfig/security from another sles9 install (/usr/bin/Check called by rpm would fail)""",

}


