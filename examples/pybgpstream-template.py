#!/usr/bin/env python
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
