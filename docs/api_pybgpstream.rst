pybgpstream
============

This document describes the API of the pybgpstream module, a high-level
interface to the C `libbgpstream` library, providing a more user-friendly
interaction with the low-level `_pybgpstream` API.

.. py:module:: pybgpstream

Example
----------
.. code-block:: python
   :linenos:

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
      print(elem)

   # alternatively, records and elems can be read in nested loops:
   for rec in stream.records():
      # do something with rec (e.g., choose to continue based on timestamp)
      print("Received %s record at time %d from collector %s" % (rec.type, rec.time, rec.collector))
      for elem in rec:
         # do something with rec and/or elem
         print("  Elem Type: %s" % elem.type)


BGPStream
---------

.. py:class:: BGPStream

   The BGP Stream class provides a single stream of BGP Records.



   .. py:attribute:: from_time

      Specify the beginning time of the stream.
      The time string is parsed using `dateutil.parser.parse` function.

   .. py:attribute:: until_time

      Specify the ending time of the stream
      The time string is parsed using `dateutil.parser.parse` function.

   .. py:attribute:: data_interface

      Specify the `data_interface` BGPStream should use for retrieving and processing data.

   .. py:attribute:: project

      Name of the project to retrive the data from.

   .. py:attribute:: projects

      Name of the projects to retrive the data from.

   .. py:attribute:: collector
   
      Name of the collector to retrive the data from.

   .. py:attribute:: collectors

      Name of the collectors to retrive the data from.

   .. py:attribute:: record_type

      Specify type of the record type to process: `updates`, or `ribs`.

   .. py:attribute:: record_types

      Specify type of the record types to process: `updates`, or `ribs`.

   .. py:attribute:: filter

      The filter string.
   
   .. py:method:: records()

      Returns a stream of Record objects.

BGPRecord
---------

.. py:class:: BGPRecord

   The BGPRecord is a wrapper around low-level `_pybgpstream.BGPRecord`.

   All attributes are read-only.

   .. py:attribute:: rec

      The corresponding `_pybgpstream.BGPRecord`.

   .. py:method:: __str__(self)

      .. code-block:: python
         :linenos:

         return "%s|%s|%f|%s|%s|%s|%s|%s|%d" % (self.type, self.dump_position, self.time,
                                               self.project, self.collector, self.router, self.router_ip,
                                               self.status, self.dump_time)



BGPElem
---------

.. py:class:: BGPElem


   The BGPElem is a wrapper around low-level `_pybgpstream.BGPElem`.

   All attributes are read-only.

   .. py:attribute:: record

      The BGPRecord that contains the current BGPElem.

   .. py:method:: __str__(self)

      .. code-block:: python
         :linenos:

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
