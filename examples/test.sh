#!/bin/sh
[ $1 = "-gdb" ] && DEBUG=1 && shift

if test -z $1; then
	echo
	echo "Run example program in development tree"
	echo "Use: $0 [-gdb] filename.py"
	echo "Toby D. Reeves <toby@solidstatescientific.com>"
	exit 0
fi

export PYTHONPATH=../:../gtkextra/:$PYTHONPATH

if test -z $DEBUG; then
    python2 -c "import ltihooks;del ltihooks;execfile('$1')"
else
    python2 -c "\
import ltihooks
del ltihooks
import os
raw_input('Attach gdb on %d. Press return to begin \"$1\".' % os.getpid())
del os
execfile('$1')"
fi
