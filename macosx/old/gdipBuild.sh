#!/bin/sh -x

if [ $# != 2 ]; then
    echo "This script is normally called from the buildMono.sh script"
    echo "If you want to run this standalone you must specify the"
    echo "path to your dependencies build directory and build scripts."
    echo "Example:"
    echo "./gdipBuild.sh /Users/Shared/MonoBuild/Dependancies ${PWD}"
    exit
fi


DEPS=$1
MONOBUILDFILES=$2
PATCHDIR=${MONOBUILDFILES}/libgdiplus/jpeg/files
NAME=jpeg
VERSION=6b 
DISTNAME=${NAME}src.v${VERSION}.tar.gz
URL=ftp://ftp.uu.net/graphics/jpeg/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

export CFLAGS="-I/Library/Frameworks/Mono.framework/Versions/Current/include" 
export C_INCLUDE_FLAGS="-I/Library/Frameworks/Mono.framework/Versions/Current/include"
export CPATH="/Library/Frameworks/Mono.framework/Versions/Current/include"
export DYLD_LIBRARY_PATH="/Library/Frameworks/Mono.framework/Versions/Current/lib"
export LDFLAGS="-L/Library/Frameworks/Mono.framework/Versions/Current/lib"
export PATH="/usr/X11R6/bin/:/Library/Frameworks/Mono.framework/Versions/Current/bin:$PATH"
export PKG_CONFIG_PATH=/usr/X11R6/lib/pkgconfig/:$PKG_CONFIG_PATH
export ACLOCAL_FLAGS="-I /Library/Frameworks/Mono.framework/Versions/1.1.4/share/aclocal/"

#JPEG
#################################################
cd ${DEPS}    
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L --max-redirs 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
fi
    cd ${WORKSRCDIR}
    patch config.guess ${PATCHDIR}/patch-config.guess
    patch config.sub ${PATCHDIR}/patch-config.sub
    patch ltmain.sh ${PATCHDIR}/patch-ltmain.sh
    patch ltconfig ${PATCHDIR}/patch-ltconfig

    sed -e 's/(prefix)\/man/(prefix)\/share\/man/g' makefile.cfg > makefile.cfg.patched
    mv makefile.cfg.patched makefile.cfg

    ./configure --enable-shared --enable-static --prefix=${MONOPREFIX}
    make
make install


################################
PATCHDIR=${MONOBUILDFILES}/libgdiplus/tiff/files
NAME=tiff
VERSION=3.7.1
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=ftp://ftp.freebsd.org/pub/FreeBSD/ports/distfiles/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L --max-redirs 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}
fi
    ./configure --prefix=${MONOPREFIX} --mandir=${MONOPREFIX}/share/man \
	--with-jpeg-include-dir=${MONOPREFIX}/include \
	--with-jpeg-lib-dir=${MONOPREFIX}/lib
    make 
    make install


###############################################
#PATCHDIR=${MONOBUILDFILES}/libgdiplus/tiff/files
NAME=libpng
VERSION=1.2.8
DISTNAME=${NAME}-${VERSION}-config.tar.gz

URL=http://easynews.dl.sourceforge.net/sourceforge/libpng/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}-config
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current
cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L --max-redirs 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}
fi
    #cp scripts/makefile.darwin Makefile
    ./configure --prefix=${MONOPREFIX}
    #sed -e "s/\/usr\/local/\${MONOPREFIX}/g" Makefile > Makefile.patched
    #sed -e 's/(prefix)\/man/(prefix)\/share\/man/g' makefile.cfg > makefile.cfg.patched
    #mv Makefile.patched Makefile

    make
    make install


###############################################
#PATCHDIR=${MONOBUILDFILES}/libgdiplus/tiff/files
NAME=libungif
VERSION=4.1.3
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://easynews.dl.sourceforge.net/sourceforge/libungif/libungif-4.1.3.tar.gz
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current                                       
cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L --max-redirs 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}
fi
    ./configure --prefix=${MONOPREFIX}
    make
    make install


###############################################
NAME=libgdiplus
VERSION=1.1.5
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://www.go-mono.com/archive/1.1.5/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

echo "building libgdiplus"

cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    if [ ! -e ${DEPS}/${DISTNAME} ];then
	curl -L --max-redirs 5 -s -O ${URL}
	gnutar -xzf ${DISTNAME}
    fi

fi
    cd ${WORKSRCDIR}
    ./configure --prefix=${MONOPREFIX} --with-libjpeg --includedir=${MONOPREFIX}/include
    make
    make install

#http://www.go-mono.com/archive/1.1.5/libgdiplus-1.1.5.tar.gz