# require automake-1.5
AUTOMAKE_OPTIONS = 1.5

SUBDIRS = gtkextra

CLEANFILES =
EXTRA_DIST = 

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = python-gtkextra.pc

noinst_PYTHON = ltihooks.py

EXTRA_DIST += \
  python-gtkextra.spec \
  python-gtkextra.spec.in \
  python-gtkextra-2.0.pc.in

snap:
	$(MAKE) dist distdir=$(PACKAGE)-SNAP-`date +"%Y%m%d"`
