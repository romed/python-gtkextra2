pygtkextradir = $(pythondir)/gtkextra
pygtkextra_PYTHON = __init__.py

pygtkextraexecdir = $(pyexecdir)/gtkextra

# FIXME: Do we want to drop files in the pygtk directory or in our own pkg directory
defsdir = $(PYGTK_DEFSDIR)
defs_DATA =
EXTRA_DIST = $(defs_DATA)
CLEANFILES =

pkgincludedir = $(includedir)/pygtkextra-2.0/pygtkextra
pkginclude_HEADERS = 

INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES) -Wall
#COMMONDEFS = $(srcdir)/gtkextra-types.defs 
COMMONDEFS = 

# gtkextra module
#GTKEXTRA_LIBS=-lgtkextra #DOES NOT WORK
#GTKEXTRA_LIBS=-lgtkextra-x11 #DOES NOT WORK
pygtkextraexec_LTLIBRARIES = gtkextramodule.la
gtkextramodule_la_CFLAGS = $(PYGTK_CFLAGS) $(GTK_CFLAGS) $(GTKEXTRA_CFLAGS)
gtkextramodule_la_LDFLAGS = -module -avoid-version -export-symbols-regex initgtkextra
gtkextramodule_la_LIBADD =  $(GTKEXTRA_LIBS) $(PYGTK_LIBS) $(GTK_LIBS)
gtkextramodule_la_SOURCES = gtkextramodule.c
gtkextra.c: $(COMMONDEFS) gtkextra.override
nodist_gtkextramodule_la_SOURCES = gtkextra.c

CLEANFILES += gtkextra.c
defs_DATA += gtkextra.defs
EXTRA_DIST += gtkextra.override

.defs.c:
	(cd $(srcdir) \
	 && $(PYTHON) $(PYGTK_DEFSDIR)/../codegen/codegen.py \
	    --register $(PYGTK_DEFSDIR)/pango-types.defs \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $*.override \
	    --prefix py$* $*.defs) > gen-$*.c \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c

