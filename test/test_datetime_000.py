# -*- coding: utf-8 -*-

import unittest
import sys
import os


import MythTV
from datetime import datetime as _pytzdt
from datetime import timedelta
import time
from MythTV import datetime


class test_datetime_000(unittest.TestCase):
    """Test basic 'datetime' functionality of MythTV.utilities.dt."""

    @classmethod
    def setUpClass(cls):
        """ Get time data for testing:
        # run timedatectl and extract local-time, utc-time and time-zone offset
        # get current timestamp:
        # $ date +%s.%N

        $ timedatectl
                              Local time: Sat 2020-05-30 12:53:26 CEST
                          Universal time: Sat 2020-05-30 10:53:26 UTC
                                RTC time: Sat 2020-05-30 10:53:26
                               Time zone: Europe/Vienna (CEST, +0200)
               System clock synchronized: yes
        systemd-timesyncd.service active: yes
                         RTC in local TZ: no
        """


        import subprocess

        cmd = "timedatectl"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        #print(out)
        cls.lt = cls.ut = cls.ot = None
        for line in out.splitlines():
            if b"Local time:" in line:
                cls.lt = line.decode().replace("Local time: ", "").strip()
            if b"Universal time:" in line:
                cls.ut = line.decode().replace("Universal time: ", "").strip()
            if b"Time zone:" in line:
                cls.ot = int(line.decode().split()[-1].replace(")","")) * 36   # offset in seconds

        print("local time:  %s" %cls.lt)    # local time:  Sat 2020-05-30 22:21:34 CEST
        print("utc time:    %s" %cls.ut)    # utc time:    Sat 2020-05-30 20:21:34 UTC
        print("time offset: %s" %cls.ot)    # time offset: 7200

        # get current timestamp
        # $ date +%s.%N
        cmd = "date +%s.%N"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        # print(out, type(out))
        cls.cts = float(out.decode())
        print("timestamp:  ", cls.cts, type(cls.cts))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_datetime_000_01(self):
        """Test method 'MythTV.datetime.localTZ()"""

        #print(self.ot, type(self.ot))
        tzlocal = datetime.localTZ()
        self.assertTrue(isinstance(tzlocal, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for local timezone")
        #print(tzlocal.utcoffset().seconds, type(tzlocal.utcoffset().seconds))
        self.assertEqual(self.ot, tzlocal.utcoffset().seconds, "NO offset calculation possible for 'tzlocal'")


    def test_datetime_000_02(self):
        """test method 'MythTV.datetime.UTCTZ()'"""

        utctz = datetime.UTCTZ()
        self.assertTrue(isinstance(utctz, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for 'ETC/UTC' timezone")
        self.assertEqual(utctz.utcoffset().seconds, 0, "ofsset to 'UTC' is not '0'")


    def test_datetime_000_03(self):
        """test method 'MythTV.datetime.fromDatetime()' without tzinfo"""

        t1 = _pytzdt(2020, 1, 2, 3, 4, 5)
        #print(t1, type(t1))
        #print(dir(t1))
        #print(t1.utcoffset())
        # print(t1.utcoffset().seconds)   ---> traceback
        self.assertIsNone(t1.utcoffset(), "Python's 'datetime' objects has no 'utcoffset'")

        t_fromDatetime = datetime.fromDatetime(t1)
        #print(t_fromDatetime, type(t_fromDatetime))
        #print(dir(t_fromDatetime))
        #print(dir(t_fromDatetime.utcoffset()))
        #print(t_fromDatetime.utcoffset().seconds)
        #print(type(t_fromDatetime.utcoffset()))
        self.assertTrue(isinstance(t_fromDatetime.utcoffset(), timedelta), "'utcoffset' error")


    def test_datetime_000_04(self):
        """test method 'MythTV.datetime.fromDatetime()' with tzinfo"""

        t2 = _pytzdt(2020, 8, 9, 10, 11, 12)
        self.assertIsNone(t2.utcoffset(), "Python's 'datetime' objects has no 'utcoffset'")
        t_fromDatetime = datetime.fromDatetime(t2, tzinfo = datetime.UTCTZ())
        #print(t_fromDatetime, type(t_fromDatetime))
        #print(t_fromDatetime.utcoffset().seconds)
        self.assertEqual(t_fromDatetime.utcoffset().seconds, 0, "MythTV's 'UTC' time has an offset of zero ('0')")


    def test_datetime_000_05(self):
        """Test method 'MythTV.datetime.now()' without tzinfo"""

        t3 = datetime.now()
        #print(t3, type(t3))
        #print(dir(t3))
        self.assertTrue(isinstance(t3.tzinfo, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for 'datetime.now()")
        #print(t3.utcoffset().seconds)
        self.assertEqual(self.ot, t3.utcoffset().seconds, "NO time-zone offset calculation possible for 'dateime.now'")


    def test_datetime_000_06(self):
        """Test method 'MythTV.datetime.now()' with tzinfo"""

        utctz = datetime.UTCTZ()
        t4 = datetime.now(tz=utctz)
        #print(t4, type(t4))
        #print(dir(t4))
        self.assertTrue(isinstance(t4.tzinfo, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for 'datetime.now()")
        #print(t4.utcoffset().seconds)
        self.assertEqual(t4.utcoffset().seconds, 0, "MythTV's 'datetime.now, tz = UTC' time has an offset")


    def test_datetime_000_07(self):
        """Test method 'MythTV.datetime.utcnow()'"""

        utctz = datetime.UTCTZ()
        t4 = datetime.now(tz=utctz)
        t5 = datetime.utcnow()
        #print(t5, type(t5))
        #print(t4, type(t4))
        """
        2020-05-29 20:31:19.914221+00:00
        2020-05-29 20:31:19.913824+00:00
        """
        #print(timedelta(t4,t5))  # does not work
        deltatime = t5 -t4
        #print(deltatime, type(deltatime))                # <class 'datetime.timedelta'>
        #print(deltatime.seconds, deltatime.microseconds)

        self.assertTrue((deltatime < timedelta(seconds = 1)), "Wrong implementation of 'utc(now)'")


    def test_datetime_000_08(self):
        """Test method 'MythTV.datetime.utcnow()' against output of 'timedatectl'"""

        t6 = datetime.utcnow()
        dt7 = self.ut.split(" ", 1)[1]
        dt7 = dt7.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt7, tz = 'UTC')
        #print(dtiso)
        self.assertTrue(((t6 - dtiso) < timedelta(seconds=1)),  "Wrong implementation of 'utc(now)'")


    def test_datetime_000_09(self):
        """Test method 'MythTV.datetime.fromtimestamp()' without given time-zone"""

        ct0 = time.time()
        #print(ct0,type(ct0))
        try:
            ct1 = _pytzdt.now().timestamp()      # python 3.x
        except AttributeError:
            # python2 does not have a 'datetime.timestamp':
            ct1 = time.time()                    # python 2.7

        self.assertTrue((abs(ct1 - ct0) < 0.01), "Timestamp values different in 'datetime.timestamp' and 'time.timestamp'")

        #print(ct1, type(ct1))
        # MythTV's datetime implementation:
        ct2 = datetime.now().timestamp()
        #print(ct2, type(ct2))               # 1590849753.5594988 <class 'float'>

        self.assertTrue((abs(ct2 - ct1) < 0.01), "Timestamp values different in 'MythTV' and 'datetime'")
        self.assertTrue((abs(ct2 - self.cts) < 0.1), "Timestamp values different in 'MythTV' and  linux 'date +%s.%N'")

        cf1 = datetime.fromtimestamp(ct2)
        #print(cf1, type(cf1))  #  2020-05-30 17:23:51.551984+02:00 <class 'MythTV.utility.dt.datetime'>
        self.assertTrue(isinstance(cf1.tzinfo, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for 'datetime.fromtimestamp()")
        t8 = datetime.now()
        #print(t8, type(t8))
        self.assertTrue((abs(t8 - cf1) < timedelta(seconds=1)), "'datetime.fromtimestamp()' values different in 'MythTV' and  linux 'date +%s.%N'")


    def test_datetime_000_10(self):
        """Test method 'MythTV.datetime.fromtimestamp()' with given time-zone"""

        # MythTV's datetime implementation:
        utctz = datetime.UTCTZ()
        ct3 = datetime.now(tz=utctz).timestamp()
        #print(ct3, type(ct3))
        t9 = datetime.utcnow().timestamp()
        #print(t9, type(t9))
        self.assertTrue((abs(ct3 - self.cts) < 0.01), "wrong implementation of 'datetime.now(tz=utctz).timestamp()'")
        self.assertTrue((abs(t9 - self.cts) < 0.01), "wrong implementation of 'datetime.now(tz=utctz).timestamp()'")

        tzlocal = datetime.localTZ()
        cf2 = datetime.fromtimestamp(ct3, tz = tzlocal)
        #print(cf2, type(cf2))
        t10 = datetime.now()
        self.assertTrue(isinstance(cf2.tzinfo, MythTV.utility.dt.posixtzinfo), "No posixtzinfo for 'datetime.fromtimestamp()")
        self.assertTrue(((cf2 -t10) < timedelta(microseconds = 100)), "wrong implementation of 'datetime.now(tz=utctz).timestamp()'")


    def test_datetime_000_11(self):
        """Test method 'MythTV.datetime.utcfromtimestamp()"""

        utctz = datetime.UTCTZ()
        # get the local datetime
        ct4 = _pytzdt.now()
        #print(ct4, type(ct4))
        # replace tzinfo
        ct4 = ct4.replace(tzinfo=utctz)
        # subtract offset-time retrieved from 'timedatectl'
        ct4 = ct4 - timedelta(seconds=self.ot)
        #print(ct4, type(ct4))
        t11 = datetime.utcfromtimestamp(self.cts)
        #print(t11, type(t11))
        self.assertTrue(((ct4 - t11) < timedelta(seconds = 1)), "wrong implementation of 'datetime.now(tz=utctz).utctimestamp()'")


    def test_datetime_000_12(self):
        """Test method 'MythTV.datetime.strptime()' without timezone"""

        ts1 = datetime.strptime(self.lt, '%a %Y-%m-%d %H:%M:%S %Z')  #    Sat 2020-05-30 22:06:46 CEST
        #print(ts1, type(ts1))                                  #        2020-05-30 22:06:46+02:00 <class 'MythTV.utility.dt.datetime'>
        ts1_str = str(ts1).split("+")[0]
        #print(ts1_str)                                         # 2020-05-30 22:06:46
        self.assertTrue(isinstance(ts1, MythTV.utility.dt.datetime), "Instance ''MythTV.datetime.strptime()' is not available")

        dt8 = self.lt.split(" ", 1)[1]
        dt8 = dt8.rsplit(" ", 1)[0]
        #print(dt8)
        self.assertEqual(ts1_str, dt8, "Instance ''MythTV.datetime.strptime()' for local-time is wrong")

        ts2 = datetime.strptime(self.ut, '%a %Y-%m-%d %H:%M:%S %Z')  #   Sat 2020-05-30 20:06:46 UTC
        #print(ts2, type(ts2))                                  #       2020-05-30 20:06:46+02:00 <class 'MythTV.utility.dt.datetime'>
        ts2_str = str(ts2).split("+")[0]

        dt9 = self.ut.split(" ", 1)[1]
        dt9 = dt9.rsplit(" ", 1)[0]
        #print(dt9)
        self.assertEqual(ts2_str, dt9, "Instance ''MythTV.datetime.strptime()' for utc-time is wrong")


    def test_datetime_000_13(self):
        """Test method 'MythTV.datetime.strptime()' with given timezone"""

        slt = self.lt.rsplit(" ",1)[0]
        dt9 = slt.split(" ",1)[1]
        #print(slt)
        tzlocal = datetime.localTZ()
        ts3 = datetime.strptime(slt, '%a %Y-%m-%d %H:%M:%S', tzlocal)
        #print(ts3, type(ts3))                         # 2020-05-31 11:03:51+02:00 <class 'MythTV.utility.dt.datetime'>
        ts3_str = str(ts3).split("+")[0]
        #print(ts3_str)
        self.assertTrue(isinstance(ts3, MythTV.utility.dt.datetime), "Instance ''MythTV.datetime.strptime()' is not available")
        self.assertEqual(ts3_str, dt9, "Instance ''MythTV.datetime.strptime()' for local-time is wrong")

        sut = self.ut.rsplit(" ",1)[0]
        dt10 = sut.split(" ",1)[1]
        #print(sut)
        utctz = datetime.UTCTZ()
        ts4 = datetime.strptime(sut, '%a %Y-%m-%d %H:%M:%S', utctz)
        #print(ts4, type(ts4))                         # 2020-05-31 11:03:51+02:00 <class 'MythTV.utility.dt.datetime'>
        ts4_str = str(ts4).split("+")[0]
        #print(ts4_str)
        self.assertTrue(isinstance(ts4, MythTV.utility.dt.datetime), "Instance ''MythTV.datetime.strptime()' is not available")
        self.assertEqual(ts4_str, dt10, "Instance ''MythTV.datetime.strptime()' for local-time is wrong")


    def test_datetime_000_14(self):
        """Test method 'MythTV.datetime.fromnaiveutc(cls, dt)()'"""

        dt12 = datetime(2020, 1, 2, 3, 4, 5)
        dt12.replace(tzinfo = None)
        #print(dt12, type(dt12))
        dt13 = datetime.fromnaiveutc(dt12)
        #print(dt13, type(dt13))
        #print(dt13.utcoffset(), type(dt13.utcoffset()))
        self.assertEqual((dt13 - dt12), dt13.utcoffset(), "'fromnaiveutc()' returned wrong offset")


    def test_datetime_000_15(self):
        """Test method 'MythTV.datetime.frommythtime(cls, mtime, tz=None)"""

        dt14_int = 20200102030405
        dt14 = datetime.frommythtime(dt14_int)
        #print(dt14, type(dt14))
        #print(dt14.utcoffset())
        dt15 = datetime.frommythtime(dt14_int, tz = 'UTC')
        #print(dt15, type(dt15))
        self.assertEqual((dt15 - dt14), dt14.utcoffset(), "'frommythtime()' returned wrong offset")


    def test_datetime_000_16(self):
        """Test method 'MythTV.datetime.mythformat"""

        dt16_int = 20200102030405
        dt16 = datetime.frommythtime(dt16_int, tz = 'UTC')
        dt17 = dt16.mythformat()
        #print(dt17, type(dt17))
        self.assertEqual(dt16_int, int(dt17), "'mythformat()' returned wrong stamp")


    def test_datetime_000_17(self):
        """Test method 'MythTV.datetime.timestamp()"""

        dt20 = self.ut.split(" ", 1)[1]
        dt20 = dt20.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt20, tz = 'UTC')
        tstamp = dtiso.timestamp()
        #print(tstamp)
        self.assertTrue((abs(tstamp - self.cts) < 1.0), "'datetime.timestamp()' delivers wrong stamp")

        dt21 = self.lt.split(" ", 1)[1]
        dt21 = dt21.rsplit(" ", 1)[0]
        dtiso1 = datetime.fromIso(dt21)
        tstamp1 = dtiso1.timestamp()
        #print(tstamp1)
        self.assertTrue((abs(tstamp1 - self.cts) < 1.0), "'datetime.timestamp()' delivers wrong stamp")


    def test_datetime_000_18(self):
        """Test method 'MythTV.datetime.rfcformat()"""

        dt22 = self.ut.split(" ", 1)[1]
        dt22 = dt22.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt22, tz = 'UTC')
        trfc = dtiso.rfcformat()
        #print(trfc)                            # Sun, 31 May 2020 11:10:44 +0000

        dt23 = self.lt.split(" ", 1)[1]
        dt23 = dt23.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt23)
        trfc1 = dtiso.rfcformat()
        #print(trfc1)                           # Sun, 31 May 2020 13:10:44 +0200

        dttrfc = datetime.duck(trfc)
        dttrfc1 = datetime.duck(trfc1)

        #print(dttrfc)
        #print(dttrfc1)

        self.assertTrue(isinstance(dttrfc,MythTV.utility.dt.datetime), "Unknown type returned from 'rfcfomat()'")
        self.assertTrue(isinstance(dttrfc,MythTV.utility.dt.datetime), "Unknown type returned from 'rfcfomat()'")

        self.assertEqual((dttrfc1 - dttrfc), timedelta(seconds = 0), "Wrong time calculated from 'rfcformat()'")


    def test_datetime_000_19(self):
        """Test method 'MythTV.datetime.utcrfcformat()"""

        dt24 = self.ut.split(" ", 1)[1]
        dt24 = dt24.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt24, tz = 'UTC')
        utrfc = dtiso.utcrfcformat()

        dt25 = self.lt.split(" ", 1)[1]
        dt25 = dt25.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt25)
        utrfc1 = dtiso.utcrfcformat()

        #print(utrfc)
        #print(utrfc1)
        self.assertEqual(utrfc, utrfc1, "Wrong time calculated from 'utcrfcformat()'")


    def test_datetime_000_20(self):
        """Test method 'MythTV.datetime.utcisoformat()"""

        dt24 = self.ut.split(" ", 1)[1]
        dt24 = dt24.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt24, tz = 'UTC')
        utiso = dtiso.utcisoformat()

        dt25 = self.lt.split(" ", 1)[1]
        dt25 = dt25.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt25)
        utiso1 = dtiso.utcisoformat()

        #print(dtiso)
        #print(dtiso1)
        self.assertEqual(utiso, utiso1, "Wrong time calculated from 'utcisoformat()'")


    def test_datetime_000_21(self):
        """Test method 'MythTV.asnaiveutc()"""

        dt24 = self.ut.split(" ", 1)[1]
        dt24 = dt24.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt24, tz = 'UTC')
        autiso = dtiso.asnaiveutc()

        dt25 = self.lt.split(" ", 1)[1]
        dt25 = dt25.rsplit(" ", 1)[0]
        dtiso = datetime.fromIso(dt25)
        autiso1 = dtiso.asnaiveutc()

        #print(autiso)
        #print(autiso1)
        self.assertEqual(autiso, autiso1, "Wrong time calculated from 'asnaiveutc()'")


    if __name__ == '__main__':
        unittest.main()

