/* -*- Mode: C; c-basic-offset: 4 -*- */
#ifdef HAVE_CONFIG_H
#  include "config.h"
#endif
#include <Python.h>
/* include this first, before NO_IMPORT_PYGOBJECT is defined */
#include <pygobject.h>
#include <pygtk/pygtk.h>
#include <gtkextra/gtkextra.h>
#include <gtkextra/gtkextratypebuiltins.h>

void pygtkextra_register_classes(PyObject *d);
void pygtkextra_add_constants(PyObject *module, const gchar *strip_prefix);

extern PyMethodDef pygtkextra_functions[];

PyTypeObject *_PyArray_Type;

DL_EXPORT(void)
init_gtkextra(void)
{
    PyObject *m, *d, *module;

    m = Py_InitModule("gtkextra._gtkextra", pygtkextra_functions);
    d = PyModule_GetDict(m);

    init_pygobject();
    init_pygtk();

    pygtkextra_register_classes(d);
    pygtkextra_add_constants(m, "GTK_");

    /* These were #defines's */
    PyModule_AddIntConstant(m, "PLOT_LETTER_W", GTK_PLOT_LETTER_W);
    PyModule_AddIntConstant(m, "PLOT_LETTER_H", GTK_PLOT_LETTER_H);
    PyModule_AddIntConstant(m, "PLOT_LEGAL_W", GTK_PLOT_LEGAL_W);
    PyModule_AddIntConstant(m, "PLOT_LEGAL_H", GTK_PLOT_LEGAL_H);
    PyModule_AddIntConstant(m, "PLOT_A4_W", GTK_PLOT_A4_W);
    PyModule_AddIntConstant(m, "PLOT_A4_H", GTK_PLOT_A4_H);
    PyModule_AddIntConstant(m, "PLOT_EXECUTIVE_W", GTK_PLOT_EXECUTIVE_W);
    PyModule_AddIntConstant(m, "PLOT_EXECUTIVE_H", GTK_PLOT_EXECUTIVE_H);
    PyModule_AddIntConstant(m, "PLOT_CANVAS_DND_FLAGS", GTK_PLOT_CANVAS_DND_FLAGS);

    /* These were anonymous enum's. They really should be fixed in gtkextra. */
    PyModule_AddIntConstant(m, "ICON_LIST_ICON", GTK_ICON_LIST_ICON);
    PyModule_AddIntConstant(m, "ICON_LIST_TEXT_RIGHT", GTK_ICON_LIST_TEXT_RIGHT);
    PyModule_AddIntConstant(m, "ICON_LIST_TEXT_BELOW", GTK_ICON_LIST_TEXT_BELOW);


    if ((module = PyImport_ImportModule("array")) != NULL) {
        PyObject *moddict = PyModule_GetDict(module);
        _PyArray_Type = (PyTypeObject *)PyDict_GetItemString(moddict, "ArrayType");
    } 
    else {
        Py_FatalError("could not import array");
        return;
    }
    

    if (PyErr_Occurred())
        Py_FatalError("could not initialise module gtkextra._gtkextra");
}
