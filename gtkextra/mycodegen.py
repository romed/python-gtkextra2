#!/bin/env python

# This is a temporary hack.
import sys
sys.path.append('/usr/share/pygtk/2.0/')
del sys

# Use the PyGtk2 codegen modules
from codegen.argtypes import matcher
import codegen.codegen


matcher.register('GdkWChar', matcher.get('gint32'))

codegen.codegen.main()

