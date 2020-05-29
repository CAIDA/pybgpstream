from unittest import TestCase

from pybgpstream import BGPStream


class TestBGPStream(TestCase):
    """
    Test PyBGPStream
    """

    def test_singlefile_interface(self):
        """
        Test "singlefile" interface for PyBGPStream
        :return:
        """
        stream = BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "upd-file",
                                         "http://routeviews.org/route-views.sg/bgpdata/2020.05/UPDATES/updates.20200501.0000.bz2")
        elem_cnt = 0
        for _ in stream:
            elem_cnt += 1
        self.assertEqual(213692, elem_cnt)

    def test_filters(self):
        """
        Test filter strings for PyBGPStream
        """
        stream = BGPStream(
            from_time="2017-07-07 00:00:00", until_time="2017-07-07 00:10:00 UTC",
            collectors=["route-views.sg", "route-views.eqix"],
            record_type="updates",
            filter="peer 11666 and prefix more 210.180.0.0/16"
        )
        elem_cnt = 0
        for _ in stream:
            elem_cnt += 1
        self.assertEqual(11, elem_cnt)
