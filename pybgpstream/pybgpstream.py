# This file is part of pybgpstream
#
# CAIDA, UC San Diego
# bgpstream-info@caida.org
#
# Copyright (C) 2015 The Regents of the University of California.
# Authors: Alistair King
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

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
