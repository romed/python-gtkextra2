#!/bin/sh
[ $1 = "-gdb" ] && DEBUG=1 && shift

if test -z $1; then
	echo
	echo "Run example program in development tree"
	echo "Use: $0 [-gdb] filename.py"
	echo "Toby D. Reeves <toby@solidstatescientific.com>"
	exit 0
fi

export PYTHONPATH=../:$PYTHONPATH

if test -z $DEBUG; then
    python -c "import common;execfile('$1')"
else
    python -c "\
import common
import os
raw_input('Attach gdb on %d. Press return to begin \"$1\".' % os.getpid())
del os
execfile('$1')"
fi
