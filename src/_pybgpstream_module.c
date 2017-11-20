/*
 * Copyright (C) 2015 The Regents of the University of California.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include "_pybgpstream_bgpelem.h"
#include "_pybgpstream_bgprecord.h"
#include "_pybgpstream_bgpstream.h"
#include <Python.h>

static PyMethodDef module_methods[] = {
  {NULL} /* Sentinel */
};

#define ADD_OBJECT(objname)                                                    \
  do {                                                                         \
    if ((obj = _pybgpstream_bgpstream_get_##objname##Type()) == NULL)          \
      return NULL;                                                             \
    if (PyType_Ready(obj) < 0)                                                 \
      return NULL;                                                             \
    Py_INCREF(obj);                                                            \
    PyModule_AddObject(m, #objname, (PyObject *)obj);                          \
  } while (0)

#define MODULE_DOCSTRING                                                       \
  "Module that provides a low-level interface to libbgpstream"

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef module_def = {
  PyModuleDef_HEAD_INIT,
  "_pybgpstream",
  MODULE_DOCSTRING,
  -1,
  module_methods,
  NULL,
  NULL,
  NULL,
  NULL,
};
#endif

#ifndef PyMODINIT_FUNC /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

static PyObject *moduleinit(void)
{
  PyObject *m;
  PyTypeObject *obj;

#if PY_MAJOR_VERSION > 2
  m = PyModule_Create(&module_def);
#else
  m = Py_InitModule3("_pybgpstream", module_methods, MODULE_DOCSTRING);
#endif

  if (m == NULL)
    return NULL;

  /* BGPStream object */
  ADD_OBJECT(BGPStream);

  /* BGPRecord object */
  ADD_OBJECT(BGPRecord);

  /* BGPRecord object */
  ADD_OBJECT(BGPElem);

  return m;
}

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit__pybgpstream(void)
{
  return moduleinit();
}
#else
PyMODINIT_FUNC init_pybgpstream(void)
{
  moduleinit();
}
#endif
