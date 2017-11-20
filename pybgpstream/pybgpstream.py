#
# Copyright (C) 2017 The Regents of the University of California.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import datetime
import dateutil.parser
import _pybgpstream


class BGPStream:

    def __init__(self,
                 from_time=None,
                 until_time=None,
                 data_interface=None,
                 project=None,
                 projects=None,
                 collector=None,
                 collectors=None,
                 record_type=None,
                 record_types=None,
                 filter=None,
                 ):
        # create a low-level bgpstream instance
        self.stream = _pybgpstream.BGPStream()

        # pass along any config options the user asked for

        # time interval (accepts string date/times)
        from_epoch = self._datestr_to_epoch(from_time)
        until_epoch = self._datestr_to_epoch(until_time)
        if from_epoch or until_epoch:
            self.stream.add_interval_filter(from_epoch, until_epoch)

        if data_interface is not None:
            self.stream.set_data_interface(data_interface)

        self._maybe_add_filter("project", project, projects)
        self._maybe_add_filter("collector", collector, collectors)
        self._maybe_add_filter("record-type", record_type, record_types)

        if filter is not None:
            self.stream.parse_filter_string(filter)

        self.started = False

    def __iter__(self):
        for _rec in self.records():
            for _elem in _rec:
                yield _elem

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

    def records(self):
        if not self.started:
            self.stream.start()
            self.started = True
        while True:
            _rec = self.stream.get_next_record()
            if _rec is None:
                return
            yield BGPRecord(_rec)

    def _maybe_add_filter(self, fname, f_single, f_list):
        if f_list is None:
            f_list = []
        if f_single is not None:
            f_list.append(f_single)
        for f in f_list:
            self.stream.add_filter(fname, f)

    @staticmethod
    def _datestr_to_epoch(datestr):
        if datestr is None:
            return 0
        dt = dateutil.parser.parse(datestr, ignoretz=True)
        return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())


class BGPRecord:

    def __init__(self, rec):
        self.rec = rec

    def __iter__(self):
        while True:
            _elem = self.rec.get_next_elem()
            if _elem is None:
                return
            yield BGPElem(self, _elem)

    def __getattr__(self, attr):
        return getattr(self.rec, attr)

    def __str__(self):
        return "%s|%s|%f|%s|%s|%s|%s|%s|%d" % (self.type, self.dump_position, self.time,
                                               self.project, self.collector, self.router, self.router_ip,
                                               self.status, self.dump_time)


class BGPElem:

    def __init__(self, rec, elem):
        self.record = rec
        self._elem = elem

    def __getattr__(self, attr):
        try:
            return getattr(self._elem, attr)
        except AttributeError:
            if attr == "record_type":
                attr = "type"
            return getattr(self.record, attr)

    def __str__(self):
        return "%s|%s|%f|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (
            self.record_type,
            self.type,
            self.time,
            self.project,
            self.collector,
            self.router,
            self.router_ip,
            self.peer_asn,
            self.peer_address,
            self._maybe_field("prefix"),
            self._maybe_field("next-hop"),
            self._maybe_field("as-path"),
            " ".join(self.fields["communities"]) if "communities" in self.fields else None,
            self._maybe_field("old-state"),
            self._maybe_field("new-state")
        )

    def _maybe_field(self, field):
        return self.fields[field] if field in self.fields else None
