#!/bin/sh
PYTHONPATH=../gtkextra/.libs LD_PRELOAD=/usr/lib/libgtkextra-x11-1.1.so.0 python2 $@

