#!/usr/bin/env python
#
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
"""
This is a sample script that uses the high-level pybgpstream module.

You can use this script as a starting point when creating new applications that use PyBGPStream
"""

import pybgpstream

# create and configure the stream
stream = pybgpstream.BGPStream(
    from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
    collectors=["route-views.sg", "route-views.eqix"],
    record_type="updates",
    filter="peer 11666 and prefix more 210.180.0.0/16"
)

# add any additional (or dynamic) filters
# e.g. from peer AS 11666 regarding the more-specifics of 210.180.0.0/16:
# stream.parse_filter_string("peer 11666 and prefix more 210.180.0.0/16")
# or using the old filter interface:
# stream.add_filter("peer-asn", "11666")
# stream.add_filter("prefix-more", "210.180.0.0/16")

# read elems
for elem in stream:
    # record fields can be accessed directly from elem
    # e.g. elem.time
    # or via elem.record
    # e.g. elem.record.time
    print elem

# alternatively, records and elems can be read in nested loops:
for rec in stream.records():
    # do something with rec (e.g., choose to continue based on timestamp)
    print "Received %s record at time %d from collector %s" % (rec.type, rec.time, rec.collector)
    for elem in rec:
        # do something with rec and/or elem
        print "  Elem Type: %s" % elem.type
