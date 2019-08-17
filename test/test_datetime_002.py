# -*- coding: utf-8 -*-

import unittest
import sys
import os


class test_datetime_002(unittest.TestCase):
    """Test basic 'datetime' functionality of MythTV.utilities.dt."""

    @classmethod
    def setUpClass(cls):
        """ Setup timezone for testing."""
        os.environ["TZ"] = "America/Anchorage"
        global datetime
        global date
        from MythTV import datetime
        from datetime import date

        ### ISO Format : YYYY-MM-DDTHH:MM:SS
        #                              AKST                   AKDT
        cls.t_iso_list     = [ "2019-01-01T20:15:00",       "2019-05-01T20:15:00" ]
        cls.t_utc_list     = [ "2019-01-01T20:15:00-09:00", "2019-05-01T20:15:00-08:00" ]
        cls.t_iso_utc_list = [ "2019-01-01T20:15:00+00:00", "2019-05-01T20:15:00+00:00" ]

        ### MythTV time notation (integer)
        #                                   AKST                   AKDT
        cls.t_mtime_list         = [ 20190101201500,               20190501201500 ]
        cls.t_mtime_utc_list     = [ "2019-01-01T20:15:00-09:00", "2019-05-01T20:15:00-08:00" ]
        cls.t_mtime_iso_utc_list = [ "2019-01-01T20:15:00+00:00", "2019-05-01T20:15:00+00:00" ]

        ### Linux timestamp notation ( seconds from 1970-01-01T00:00:00+00:00 )
        # Note: Timestamps are taken from UTC, nevertheless, python displays them in the local timezone
        #                                      AKST                     AKDT
        cls.t_timestamp_list         = [ 1546373700,                   1556741700 ]
        cls.t_timestamp_utc_list     = [ "2019-01-01T11:15:00-09:00", "2019-05-01T12:15:00-08:00" ]
        cls.t_timestamp_iso_utc_list = [ "2019-01-01T20:15:00+00:00", "2019-05-01T20:15:00+00:00" ]

        ### RFC Format : Date week day, DD month YYYY HH:MM:SS
        #                              AKST                              AKDT
        cls.t_rfc_list         = [ "Tue, 01 Jan 2019 20:15:00",       "Wed, 01 May 2019 20:15:00"       ]
        cls.t_rfc_utc_list     = [ "Tue, 01 Jan 2019 20:15:00 -0900", "Wed, 01 May 2019 20:15:00 -0800" ]
        cls.t_iso_rfc_utc_list = [ "Tue, 01 Jan 2019 20:15:00 +0000", "Wed, 01 May 2019 20:15:00 +0000" ]


    @classmethod
    def tearDownClass(cls):
        del os.environ["TZ"]


    def test_datetime_002_01(self):
        """Test 'ISO' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.duck()' method.
        """

        for i,t in enumerate(self.t_iso_list):
            t_duck = datetime.duck(t)
            t_org  = t_duck.isoformat()
            self.assertTrue(isinstance(t_duck, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_duck, datetime))
            self.assertTrue('posixtzinfo' in repr(t_duck.tzinfo))


    def test_datetime_002_02(self):
        """Test 'ISO' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'fromIso()' method.
        """

        for i,t in enumerate(self.t_iso_list):
            t_fromiso = datetime.fromIso(t)
            t_org  = t_fromiso.isoformat()
            self.assertTrue(isinstance(t_fromiso, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_fromiso, datetime))
            self.assertTrue('posixtzinfo' in repr(t_fromiso.tzinfo))


    def test_datetime_002_03(self):
        """Test 'ISO' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'fromIso(,tz='UTC') method.
        """

        for i,t in enumerate(self.t_iso_list):
            t_fromiso = datetime.fromIso(t, tz='UTC')
            t_org  = t_fromiso.isoformat()
            self.assertTrue(isinstance(t_fromiso, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_iso_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_fromiso, datetime))
            self.assertTrue('posixtzinfo' in repr(t_fromiso.tzinfo))


    def test_datetime_002_04(self):
        """Test 'mythtime (i.e. integer time)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.duck()' method.
        """

        for i,t in enumerate(self.t_mtime_list):
            t_duck = datetime.duck(t)
            t_org  = t_duck.isoformat()
            self.assertTrue(isinstance(t_duck, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_mtime_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_duck, datetime))
            self.assertTrue('posixtzinfo' in repr(t_duck.tzinfo))


    def test_datetime_002_05(self):
        """Test 'mythtime (i.e. integer time)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'frommythtime()' method.
        """

        for i,t in enumerate(self.t_mtime_list):
            t_frommythtime = datetime.frommythtime(t)
            t_org  = t_frommythtime.isoformat()
            self.assertTrue(isinstance(t_frommythtime, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_mtime_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_frommythtime, datetime))
            self.assertTrue('posixtzinfo' in repr(t_frommythtime.tzinfo))


    def test_datetime_002_06(self):
        """Test 'mythtime (i.e. integer time)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'frommythtime(,tz='UTC')' method.
        """

        for i,t in enumerate(self.t_mtime_list):
            t_frommythtime = datetime.frommythtime(t, tz='UTC')
            t_org  = t_frommythtime.isoformat()
            self.assertTrue(isinstance(t_frommythtime, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_mtime_iso_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_frommythtime, datetime))
            self.assertTrue('posixtzinfo' in repr(t_frommythtime.tzinfo))


    def test_datetime_002_07(self):
        """Test 'timestamp (i.e. seconds from epoch)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.duck()' method.
        """

        for i,t in enumerate(self.t_timestamp_list):
            t_duck = datetime.duck(t)
            t_org  = t_duck.isoformat()
            self.assertTrue(isinstance(t_duck, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_timestamp_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_duck, datetime))
            self.assertTrue('posixtzinfo' in repr(t_duck.tzinfo))


    def test_datetime_002_08(self):
        """Test 'timestamp (i.e. seconds from epoch)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.fromtimestamp()' method.
           Note: This is using the local timezone for conversion.
        """

        for i,t in enumerate(self.t_timestamp_list):
            t_ts = datetime.fromtimestamp(t)
            t_org  = t_ts.isoformat()
            self.assertTrue(isinstance(t_ts, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_timestamp_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_ts, datetime))
            self.assertTrue('posixtzinfo' in repr(t_ts.tzinfo))


    def test_datetime_002_09(self):
        """Test 'timestamp (i.e. seconds from epoch)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.fromtimestamp(,tz=datetime.UTCTZ)' method.
        """

        for i,t in enumerate(self.t_timestamp_list):
            t_ts_utc = datetime.fromtimestamp(t, tz=datetime.UTCTZ())
            t_org  = t_ts_utc.isoformat()
            self.assertTrue(isinstance(t_ts_utc, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_timestamp_iso_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_ts_utc, datetime))
            self.assertTrue('posixtzinfo' in repr(t_ts_utc.tzinfo))


    def test_datetime_002_10(self):
        """Test 'utctimestamp (i.e. seconds from epoch)' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.utcfromtimestamp()' method.
        """

        for i,t in enumerate(self.t_timestamp_list):
            t_ts_utc = datetime.utcfromtimestamp(t)
            t_org  = t_ts_utc.isoformat()
            self.assertTrue(isinstance(t_ts_utc, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_timestamp_iso_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_ts_utc, datetime))
            self.assertTrue('posixtzinfo' in repr(t_ts_utc.tzinfo))


    def test_datetime_002_11(self):
        """Test 'RFC' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'datetime.duck()' method.
        """

        for i,t in enumerate(self.t_rfc_list):
            t_duck = datetime.duck(t)
            t_org  = t_duck.rfcformat()
            self.assertTrue(isinstance(t_duck, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_rfc_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_duck, datetime))
            self.assertTrue('posixtzinfo' in repr(t_duck.tzinfo))


    def test_datetime_002_12(self):
        """Test 'RFC' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'fromRfc()' method.
        """

        for i,t in enumerate(self.t_rfc_list):
            t_fromrfc = datetime.fromRfc(t)
            t_org  = t_fromrfc.rfcformat()
            self.assertTrue(isinstance(t_fromrfc, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_rfc_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_fromrfc, datetime))
            self.assertTrue('posixtzinfo' in repr(t_fromrfc.tzinfo))


    def test_datetime_002_13(self):
        """Test 'RFC' to 'UTC' conversion in respect to daylight saving time of 'America/Anchorage'
           using 'fromRfc(,tz='UTC') method.
        """

        for i,t in enumerate(self.t_rfc_list):
            t_fromrfc = datetime.fromRfc(t, tz='UTC')
            t_org  = t_fromrfc.rfcformat()
            self.assertTrue(isinstance(t_fromrfc, datetime))
            # check if conversion works:
            self.assertEqual(t_org, self.t_iso_rfc_utc_list[i])
            # check for correct types:
            self.assertTrue(isinstance(t_fromrfc, datetime))
            self.assertTrue('posixtzinfo' in repr(t_fromrfc.tzinfo))

if __name__ == '__main__':
    unittest.main()

