GARNAME    = gluezilla
CATEGORIES = linux/mono
GARVERSION = $(GLUEZILLA_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DEPENDS  = linux/mono/mono

DESCRIPTION = GlueZilla
define BLURB
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS) --with-cairo=system

# This should go before any hand-made rules.
include ../../../gar.mk

