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

from _pybgpstream import BGPStream, BGPRecord, BGPElem

# create a new bgpstream instance
stream = BGPStream()

# create a reusable bgprecord instance
rec = BGPRecord()

# configure the stream to retrieve RIB records from the RRC06 collector at
# 2015/05/01 00:00 UTC
stream.add_filter('collector', 'rrc06')
stream.add_filter('record-type', 'ribs')
stream.add_interval_filter(1427846400, 1427846700)

# start the stream
stream.start()

as_topology = set()
rib_entries = 0

# Process data
while(stream.get_next_record(rec)):
     elem = rec.get_next_elem()
     while(elem):
         rib_entries += 1
         # get the AS path
         path = elem.fields['as-path']
         # get the list of ASes in the path
         ases = path.split(" ")
         for i in range(0,len(ases)-1):
             # avoid multiple prepended ASes
             if(ases[i] != ases[i+1]):
                 as_topology.add(tuple(sorted([ases[i],ases[i+1]])))
         # get next elem
         elem = rec.get_next_elem()

# Output results
print "Processed", rib_entries, "rib entries"
print "Found", len(as_topology), "AS adjacencies"
