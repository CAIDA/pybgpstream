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

#include "_pybgpstream_bgprecord.h"
#include "_pybgpstream_bgpelem.h"
#include "pyutils.h"
#include <Python.h>
#include <bgpstream.h>

#define BGPRecordDocstring "BGPRecord object"

static void BGPRecord_dealloc(BGPRecordObject *self)
{
  Py_TYPE(self)->tp_free((PyObject *)self);
}

static int BGPRecord_init(BGPRecordObject *self, PyObject *args, PyObject *kwds)
{
  return 0;
}

/* attributes */

#define RETURN_PYSTR_OR_NONE(cstr)                                             \
  do {                                                                         \
    if (strlen(cstr) == 0) {                                                   \
      Py_RETURN_NONE;                                                          \
    }                                                                          \
    return Py_BuildValue("s", cstr);                                           \
  } while (0)

/* project */
static PyObject *BGPRecord_get_project(BGPRecordObject *self, void *closure)
{
  RETURN_PYSTR_OR_NONE(self->rec->project_name);
}

/* collector */
static PyObject *BGPRecord_get_collector(BGPRecordObject *self, void *closure)
{
  RETURN_PYSTR_OR_NONE(self->rec->collector_name);
}

/* router */
static PyObject *BGPRecord_get_router(BGPRecordObject *self, void *closure)
{
  RETURN_PYSTR_OR_NONE(self->rec->router_name);
}

/* router_ip */
static PyObject *BGPRecord_get_router_ip(BGPRecordObject *self, void *closure)
{
  // if router IP is not set, then return None
  if (self->rec->router_ip.version == 0) {
    Py_RETURN_NONE;
  }
  // else, assume valid version, and return a string
  return get_ip_pystr((bgpstream_ip_addr_t *)&self->rec->router_ip);
}

/* type */
static PyObject *BGPRecord_get_type(BGPRecordObject *self, void *closure)
{
  switch (self->rec->type) {
  case BGPSTREAM_UPDATE:
    return Py_BuildValue("s", "update");
    break;

  case BGPSTREAM_RIB:
    return Py_BuildValue("s", "rib");
    break;

  default:
    return Py_BuildValue("s", "unknown");
  }

  return NULL;
}

/* dump_time */
static PyObject *BGPRecord_get_dump_time(BGPRecordObject *self, void *closure)
{
  return Py_BuildValue("k", self->rec->dump_time_sec);
}

/* time (sec.usec) */
static PyObject *BGPRecord_get_time(BGPRecordObject *self, void *closure)
{
  return Py_BuildValue("d", self->rec->time_sec +
                               (self->rec->time_usec / 1000000.0));
}

/* get status */
static PyObject *BGPRecord_get_status(BGPRecordObject *self, void *closure)
{
  switch (self->rec->status) {
  case BGPSTREAM_RECORD_STATUS_VALID_RECORD:
    return Py_BuildValue("s", "valid");
    break;

  case BGPSTREAM_RECORD_STATUS_FILTERED_SOURCE:
    return Py_BuildValue("s", "filtered-source");
    break;

  case BGPSTREAM_RECORD_STATUS_EMPTY_SOURCE:
    return Py_BuildValue("s", "empty-source");
    break;

  case BGPSTREAM_RECORD_STATUS_CORRUPTED_SOURCE:
    return Py_BuildValue("s", "corrupted-source");
    break;

  case BGPSTREAM_RECORD_STATUS_CORRUPTED_RECORD:
    return Py_BuildValue("s", "corrupted-record");
    break;

  default:
    return Py_BuildValue("s", "unknown");
  }

  return NULL;
}

/* get dump position */
static PyObject *BGPRecord_get_dump_position(BGPRecordObject *self,
                                             void *closure)
{
  switch (self->rec->dump_pos) {
  case BGPSTREAM_DUMP_START:
    return Py_BuildValue("s", "start");
    break;

  case BGPSTREAM_DUMP_MIDDLE:
    return Py_BuildValue("s", "middle");
    break;

  case BGPSTREAM_DUMP_END:
    return Py_BuildValue("s", "end");
    break;

  default:
    return Py_BuildValue("s", "unknown");
  }

  return NULL;
}

/* get next elem */
static PyObject *BGPRecord_get_next_elem(BGPRecordObject *self)
{
  bgpstream_elem_t *elem;
  int ret;

  PyObject *pyelem;

  ret = bgpstream_record_get_next_elem(self->rec, &elem);
  if (ret < 0) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Could not get next record (is the stream started?)");
    return NULL;
  } else if (ret == 0) {
    /* end of elems */
    Py_RETURN_NONE;
  }

  if ((pyelem = BGPElem_new(elem)) == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Could not create BGPElem object");
    return NULL;
  }

  return pyelem;
}

static PyMethodDef BGPRecord_methods[] = {

  {"get_next_elem", (PyCFunction)BGPRecord_get_next_elem, METH_NOARGS,
   "Get next BGP Elem from the Record"},

  {NULL} /* Sentinel */
};

static PyGetSetDef BGPRecord_getsetters[] = {

  {"project", (getter)BGPRecord_get_project, NULL, "Project Name", NULL},

  {"collector", (getter)BGPRecord_get_collector, NULL, "Collector Name", NULL},

  {"router", (getter)BGPRecord_get_router, NULL, "Router Name", NULL},

  {"router_ip", (getter)BGPRecord_get_router_ip, NULL, "Router IP Address", NULL},

  {"type", (getter)BGPRecord_get_type, NULL, "Type", NULL},

  {"dump_time", (getter)BGPRecord_get_dump_time, NULL, "Dump Time", NULL},

  {"time", (getter)BGPRecord_get_time, NULL, "Record Time", NULL},

  {"status", (getter)BGPRecord_get_status, NULL, "Status", NULL},

  {"dump_position", (getter)BGPRecord_get_dump_position, NULL, "Dump Position",
   NULL},

  {NULL} /* Sentinel */
};

static PyTypeObject BGPRecordType = {
  PyVarObject_HEAD_INIT(NULL, 0) "_pybgpstream.BGPRecord", /* tp_name */
  sizeof(BGPRecordObject),                                 /* tp_basicsize */
  0,                                                       /* tp_itemsize */
  (destructor)BGPRecord_dealloc,                           /* tp_dealloc */
  0,                                                       /* tp_print */
  0,                                                       /* tp_getattr */
  0,                                                       /* tp_setattr */
  0,                                                       /* tp_compare */
  0,                                                       /* tp_repr */
  0,                                                       /* tp_as_number */
  0,                                                       /* tp_as_sequence */
  0,                                                       /* tp_as_mapping */
  0,                                                       /* tp_hash */
  0,                                                       /* tp_call */
  0,                                                       /* tp_str */
  0,                                                       /* tp_getattro */
  0,                                                       /* tp_setattro */
  0,                                                       /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                /* tp_flags */
  BGPRecordDocstring,                                      /* tp_doc */
  0,                                                       /* tp_traverse */
  0,                                                       /* tp_clear */
  0,                                                       /* tp_richcompare */
  0,                        /* tp_weaklistoffset */
  0,                        /* tp_iter */
  0,                        /* tp_iternext */
  BGPRecord_methods,        /* tp_methods */
  0,                        /* tp_members */
  BGPRecord_getsetters,     /* tp_getset */
  0,                        /* tp_base */
  0,                        /* tp_dict */
  0,                        /* tp_descr_get */
  0,                        /* tp_descr_set */
  0,                        /* tp_dictoffset */
  (initproc)BGPRecord_init, /* tp_init */
  0,                        /* tp_alloc */
  0,            /* tp_new */
};

PyTypeObject *_pybgpstream_bgpstream_get_BGPRecordType()
{
  return &BGPRecordType;
}

/* only available to c code */
PyObject *BGPRecord_new(bgpstream_record_t *rec)
{
  BGPRecordObject *self;

  self = (BGPRecordObject *)(BGPRecordType.tp_alloc(&BGPRecordType, 0));
  if (self == NULL) {
    return NULL;
  }

  self->rec = rec;

  return (PyObject *)self;
}
