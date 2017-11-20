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

#ifndef ___PYUTILS_H
#define ___PYUTILS_H

#include <Python.h>

#ifndef PyVarObject_HEAD_INIT
#define PyVarObject_HEAD_INIT(type, size) PyObject_HEAD_INIT(type) size,
#endif

#if PY_MAJOR_VERSION > 2
#define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
#else
#define MOD_INIT(name) PyMODINIT_FUNC init##name(void)
#endif

#ifndef Py_TYPE
#define Py_TYPE(ob) (((PyObject *)(ob))->ob_type)
#endif

#if PY_MAJOR_VERSION > 2
#define PYSTR_FROMSTR(str) PyUnicode_FromString(str)
#define PYNUM_FROMLONG(num) PyLong_FromLong(num)
#else
#define PYSTR_FROMSTR(str) PyString_FromString(str)
#define PYNUM_FROMLONG(num) PyInt_FromLong(num)
#endif

static inline int add_to_dict(PyObject *dict, const char *key_str,
                              PyObject *value)
{
  PyObject *key = PYSTR_FROMSTR(key_str);
  int err = PyDict_SetItem(dict, key, value);
  Py_DECREF(key);
  Py_DECREF(value);
  return err;
}

static inline PyObject *get_ip_pystr(bgpstream_ip_addr_t *ip)
{
  char ip_str[INET6_ADDRSTRLEN] = "";
  bgpstream_addr_ntop(ip_str, INET6_ADDRSTRLEN, ip);
  return PYSTR_FROMSTR(ip_str);
}

#endif
