/* -*- Mode: C; c-basic-offset: 4 -*- */
#ifdef HAVE_CONFIG_H
#  include "config.h"
#endif
#include <Python.h>
/* include this first, before NO_IMPORT_PYGOBJECT is defined */
#include <pygobject.h>
#include <pygtk/pygtk.h>

void pygtkextra_register_classes(PyObject *d);
extern PyMethodDef pygtkextra_functions[];

DL_EXPORT(void)
initgtkextra(void)
{
    PyObject *m, *d;

    //m = Py_InitModule("gtkextra.gtkextra", pygtkextra_functions);
    m = Py_InitModule("gtkextra", pygtkextra_functions);
    d = PyModule_GetDict(m);

    init_pygobject();
    init_pygtk();

    pygtkextra_register_classes(d);

    if (PyErr_Occurred())
        Py_FatalError("could not initialise module gtkextra.gtkextra");
}
