/******************************************************************
 * A C extension module for Python, called "cenviron".  Wraps the
 * C library's getenv/putenv routines for use in Python programs.
 ******************************************************************/

#include <Python.h>
#include <stdlib.h>
#include <string.h>

/***********************/
/* 1) module functions */
/***********************/

static PyObject *                                   /* returns object */
wrap_getenv(PyObject *self, PyObject *args)         /* self not used */
{                                                   /* args from python */
    char *varName, *varValue;
    PyObject *returnObj = NULL;                         /* null=exception */

    if (PyArg_Parse(args, "(s)", &varName)) {           /* Python -> C */
        varValue = getenv(varName);                     /* call C getenv */
        if (varValue != NULL)
            returnObj = Py_BuildValue("s", varValue);   /* C -> Python */
        else
            PyErr_SetString(PyExc_SystemError, "Error calling getenv");
    }
    return returnObj;
}

static PyObject *
wrap_putenv(PyObject *self, PyObject *args)
{
    char *varName, *varValue, *varAssign;
    PyObject *returnObj = NULL;

    if (PyArg_Parse(args, "(ss)", &varName, &varValue))
    {
        varAssign = malloc(strlen(varName) + strlen(varValue) + 2);
        sprintf(varAssign, "%s=%s", varName, varValue);
        if (putenv(varAssign) == 0) {
            Py_INCREF(Py_None);                   /* C call success */
            returnObj = Py_None;                  /* reference None */
        }
        else
            PyErr_SetString(PyExc_SystemError, "Error calling putenv");
    }
    return returnObj;
}

/**************************/
/* 2) registration table  */
/**************************/

static PyMethodDef cenviron_methods[] = {
    {"getenv",  wrap_getenv, METH_VARARGS, "getenv doc"},  /* name, &func,... */
    {"putenv",  wrap_putenv, METH_VARARGS, "putenv doc"},  /* name, &func,... */
    {NULL, NULL, 0, NULL}                                  /* end of table marker */
};

/*************************/
/* 3) module definition  */
/*************************/

static struct PyModuleDef cenvironmodule = {
   PyModuleDef_HEAD_INIT,
   "cenviron",        /* name of module */
   "cenviron doc",    /* module documentation, may be NULL */
   -1,                /* size of per-interpreter module state, -1=in global vars */
   cenviron_methods   /* link to methods table */
};

/*************************/
/* 4) module initializer */
/*************************/

PyMODINIT_FUNC
PyInit_cenviron()                      /* called on first import */
{                                      /* name matters if loaded dynamically */
    return PyModule_Create(&cenvironmodule);
}
