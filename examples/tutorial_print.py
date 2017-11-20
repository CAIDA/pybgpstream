#!/usr/bin/env python
#
# Copyright (C) 2015 The Regents of the University of California.
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

import _pybgpstream_caida as _pybgpstream

# create a new bgpstream instance
stream = _pybgpstream.BGPStream()

# configure the stream to retrieve Updates records from the RRC06 collector
# The commented out add_filter lines are the old way, the parse_filter_string
# way is the new method for applying filters

#stream.add_filter('collector', 'rrc06')
#stream.add_filter('record-type', 'updates')
stream.parse_filter_string('collector rrc06 and type updates')

# select the time interval to process:
# Wed Apr 1 00:02:50 UTC 2015 -> Wed Apr 1 00:04:30
stream.add_interval_filter(1427846570, 1427846670)

# start the stream
stream.start()

# print the stream
rec = stream.get_next_record()
while(rec):
    print rec.status, rec.project +"."+ rec.collector, rec.time
    elem = rec.get_next_elem()
    while(elem):
        print "\t", elem.type, elem.peer_address, elem.peer_asn, \
            elem.type, elem.fields
        elem = rec.get_next_elem()
    rec = stream.get_next_record()

