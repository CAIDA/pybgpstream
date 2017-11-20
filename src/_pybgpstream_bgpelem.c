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
#include "pyutils.h"
#include <Python.h>
#include <bgpstream.h>

#define BGPElemDocstring "BGPElem object"

static PyObject *get_pfx_pystr(bgpstream_pfx_t *pfx)
{
  char pfx_str[INET6_ADDRSTRLEN + 3] = "";
  if (bgpstream_pfx_snprintf(pfx_str, INET6_ADDRSTRLEN + 3, pfx) == NULL)
    return NULL;
  return PYSTR_FROMSTR(pfx_str);
}

static PyObject *get_aspath_pystr(bgpstream_as_path_t *aspath)
{
  // assuming 10 char per ASN, then this will hold >400 hops
  char buf[4096] = "";
  if (bgpstream_as_path_snprintf(buf, 4096, aspath) >= 4096)
    return NULL;
  return PYSTR_FROMSTR(buf);
}

static PyObject *get_communities_pyset(bgpstream_community_set_t *communities)
{
  PyObject *set;
  bgpstream_community_t *c;
  int cnt = bgpstream_community_set_size(communities);
  int i;
  char comm_buf[128];
  /* create the dictionary */
  if ((set = PySet_New(NULL)) == NULL)
    return NULL;

  for (i = 0; i < cnt; i++) {
    c = bgpstream_community_set_get(communities, i);

    if (bgpstream_community_snprintf(comm_buf, sizeof(comm_buf), c) >=
        sizeof(comm_buf)) {
      return NULL;
    }

    /* add community to set */
    PySet_Add(set, PYSTR_FROMSTR(comm_buf));
  }
  return set;
}

static PyObject *get_peerstate_pystr(bgpstream_elem_peerstate_t state)
{
  char buf[128] = "";
  if (bgpstream_elem_peerstate_snprintf(buf, 128, state) >= 128)
    return NULL;
  return PYSTR_FROMSTR(buf);
}

static void BGPElem_dealloc(BGPElemObject *self)
{
  Py_XDECREF(self->fields);

  Py_TYPE(self)->tp_free((PyObject *)self);
}

static int BGPElem_init(BGPElemObject *self, PyObject *args, PyObject *kwds)
{
  return 0;
}

/* type */
static PyObject *BGPElem_get_type(BGPElemObject *self, void *closure)
{
  char buf[128] = "";
  if (bgpstream_elem_type_snprintf(buf, 128, self->elem->type) >= 128)
    return NULL;
  return PYSTR_FROMSTR(buf);
}

/* peer address */
/** @todo consider using something like netaddr
    (http://pythonhosted.org/netaddr/) */
static PyObject *BGPElem_get_peer_address(BGPElemObject *self, void *closure)
{
  return get_ip_pystr((bgpstream_ip_addr_t *)&self->elem->peer_ip);
}

/* peer as number */
static PyObject *BGPElem_get_peer_asn(BGPElemObject *self, void *closure)
{
  return Py_BuildValue("k", self->elem->peer_asn);
}

/** Type-dependent field dict */
static PyObject *BGPElem_get_fields(BGPElemObject *self, void *closure)
{
  PyObject *dict = self->fields;

  // check if we already built the dict before
  if (dict != NULL) {
    // "O" will increase refcount
    return Py_BuildValue("O", dict);
  }

  // need to create the dictionary
  if ((self->fields = dict = PyDict_New()) == NULL)
    return NULL;

  switch (self->elem->type) {
  case BGPSTREAM_ELEM_TYPE_RIB:
  case BGPSTREAM_ELEM_TYPE_ANNOUNCEMENT:
    if (add_to_dict(
          dict, "next-hop",
          get_ip_pystr((bgpstream_ip_addr_t *)&self->elem->nexthop)) ||
        add_to_dict(dict, "as-path", get_aspath_pystr(self->elem->as_path)) ||
        add_to_dict(dict, "communities",
                    get_communities_pyset(self->elem->communities))) {
      return NULL;
    }

  /* FALLTHROUGH */

  case BGPSTREAM_ELEM_TYPE_WITHDRAWAL:
    if (add_to_dict(dict, "prefix",
                    get_pfx_pystr((bgpstream_pfx_t *)&self->elem->prefix))) {
      return NULL;
    }
    break;

  case BGPSTREAM_ELEM_TYPE_PEERSTATE:
    if (add_to_dict(dict, "old-state",
                    get_peerstate_pystr(self->elem->old_state)) ||
        add_to_dict(dict, "new-state",
                    get_peerstate_pystr(self->elem->new_state))) {
      return NULL;
    }
    break;

  case BGPSTREAM_ELEM_TYPE_UNKNOWN:
  default:
    break;
  }

  return Py_BuildValue("O", dict);
}

static PyMethodDef BGPElem_methods[] = {
  {NULL} /* Sentinel */
};

static PyGetSetDef BGPElem_getsetters[] = {

  /* type */
  {"type", (getter)BGPElem_get_type, NULL, "Type", NULL},

  /* Peer Address */
  {"peer_address", (getter)BGPElem_get_peer_address, NULL, "Peer IP Address",
   NULL},

  /* peer ASN */
  {"peer_asn", (getter)BGPElem_get_peer_asn, NULL, "Peer ASN", NULL},

  /* Type-Specific Fields */
  {"fields", (getter)BGPElem_get_fields, NULL, "Type-Specific Fields", NULL},

  {NULL} /* Sentinel */
};

static PyTypeObject BGPElemType = {
  PyVarObject_HEAD_INIT(NULL, 0) "_pybgpstream.BGPElem", /* tp_name */
  sizeof(BGPElemObject),                                 /* tp_basicsize */
  0,                                                     /* tp_itemsize */
  (destructor)BGPElem_dealloc,                           /* tp_dealloc */
  0,                                                     /* tp_print */
  0,                                                     /* tp_getattr */
  0,                                                     /* tp_setattr */
  0,                                                     /* tp_compare */
  0,                                                     /* tp_repr */
  0,                                                     /* tp_as_number */
  0,                                                     /* tp_as_sequence */
  0,                                                     /* tp_as_mapping */
  0,                                                     /* tp_hash */
  0,                                                     /* tp_call */
  0,                                                     /* tp_str */
  0,                                                     /* tp_getattro */
  0,                                                     /* tp_setattro */
  0,                                                     /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,              /* tp_flags */
  BGPElemDocstring,                                      /* tp_doc */
  0,                                                     /* tp_traverse */
  0,                                                     /* tp_clear */
  0,                                                     /* tp_richcompare */
  0,                                                     /* tp_weaklistoffset */
  0,                                                     /* tp_iter */
  0,                                                     /* tp_iternext */
  BGPElem_methods,                                       /* tp_methods */
  0,                                                     /* tp_members */
  BGPElem_getsetters,                                    /* tp_getset */
  0,                                                     /* tp_base */
  0,                                                     /* tp_dict */
  0,                                                     /* tp_descr_get */
  0,                                                     /* tp_descr_set */
  0,                                                     /* tp_dictoffset */
  (initproc)BGPElem_init,                                /* tp_init */
  0,                                                     /* tp_alloc */
  0,                                                     /* tp_new */
};

PyTypeObject *_pybgpstream_bgpstream_get_BGPElemType()
{
  return &BGPElemType;
}

/* only available to c code */
PyObject *BGPElem_new(bgpstream_elem_t *elem)
{
  BGPElemObject *self;

  self = (BGPElemObject *)(BGPElemType.tp_alloc(&BGPElemType, 0));
  if (self == NULL) {
    return NULL;
  }

  self->elem = elem;

  return (PyObject *)self;
}
