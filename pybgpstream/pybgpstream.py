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
            print "%s,%s" % (from_epoch, until_epoch)
            self.stream.add_interval_filter(from_epoch, until_epoch)

        self._maybe_add_filter("project", project, projects)
        self._maybe_add_filter("collector", collector, collectors)
        self._maybe_add_filter("record-type", record_type, record_types)

        if filter is not None:
            self.stream.parse_filter_string(filter)

        self.stream.start()

    def __iter__(self):
        for _rec in self.records():
            for _elem in _rec:
                yield (_rec, _elem)

    def __getattr__(self, attr):
        try:
            return getattr(self.stream, attr)
        except AttributeError:
            return object.__getattr__(self, attr)

    def records(self):
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
            yield BGPElem(_elem)

    def __getattr__(self, attr):
        try:
            return getattr(self.rec, attr)
        except AttributeError:
            return object.__getattr__(self, attr)


class BGPElem:

    def __init__(self, elem):
        self.elem = elem

    def __getattr__(self, attr):
        try:
            return getattr(self.elem, attr)
        except AttributeError:
            return object.__getattr__(self, attr)
