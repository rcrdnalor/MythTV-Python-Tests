# -*- coding: utf-8 -*-

import unittest

import MythTV
from MythTV import Frontend

import time
import os
from datetime import timedelta

from test.helpers import tailandgrep, get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Methodheap_Frontend_001(unittest.TestCase):
    """Test methods from MythTV.Frontend().
       See https://www.mythtv.org/wiki/Frontend_control_socket
       """
    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        # connect to frontend
        self.fe = Frontend("%s" %(self.testenv['FRONTENDIP']), 6546)

    def tearDown(self):
        # close frontend
        self.fe.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/screenshot'):
            os.remove('/tmp/screenshot')
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')


    def test_Methodheap_Frontend_001_query_play_01(self):
        """Test 'sendQuery', 'sendPlay' and 'jump' methods from MythTV.Frontend()
        """

        # jump to MythVideo
        j1 = self.fe.jump.mythvideo
        self.assertTrue(j1)
        time.sleep(5)

        # Jump to 'TV Recording Playback',
        loc = self.fe.sendQuery('location')
        if (loc != 'playbackbox'):
            self.fe.jump['playbackrecordings']
            time.sleep(10)

        # Select recordings
        k1 = self.fe.key['enter']
        self.assertTrue(k1)
        time.sleep(1)

        # play first recording
        k2 = self.fe.key['enter']
        self.assertTrue(k2)
        time.sleep(10)

        # stop playback of recording
        self.fe.sendPlay('stop')
        time.sleep(2)

        loc = self.fe.sendQuery('location')
        self.assertTrue(loc == 'playbackbox')

        # Clear bookmark caused by 'stop'
        k3= self.fe.key.enter
        self.assertTrue(k3)
        time.sleep(10)
        k4 = self.fe.key.escape
        self.assertTrue(k4)


    def test_Methodheap_Frontend_001_getQuery_01(self):
        """Test 'getQuery'' methods from MythTV.Frontend().
        """
        q = self.fe.getQuery()
        # 'q' reports a list of tuples
        self.assertTrue('recordings' in [ key for (key, desc) in q])


    def test_Methodheap_Frontend_001_getPlay_01(self):
        """Test 'getPlay'' methods from MythTV.Frontend().
        """
        q = self.fe.getPlay()
        # 'q' reports a list of tuples
        self.assertTrue('seek beginning' in [ key for (key, desc) in q])


    def test_Methodheap_Frontend_001_getLoad_01(self):
        """Test 'getLoad' methods from MythTV.Frontend().
        """
        q = self.fe.getLoad()
        self.assertTrue(isinstance(q, tuple))
        self.assertTrue(isinstance(q[0], float))


    def test_Methodheap_Frontend_001_getUptime_01(self):
        """Test 'getUptime' methods from MythTV.Frontend().
        """
        q = self.fe.getUptime()
        self.assertTrue(isinstance(q, timedelta))


    def test_Methodheap_Frontend_001_getTime_01(self):
        """Test 'getTime' methods from MythTV.Frontend().
        """
        q = self.fe.getTime()
        self.assertTrue(isinstance(q, MythTV.utility.dt.datetime))


    def test_Methodheap_Frontend_001_getMemory_01(self):
        """Test 'getTime' methods from MythTV.Frontend().
        """
        q = self.fe.getMemory()
        # print(type(q['totalmem'])) --> 'future.types.newint.newint'
        self.assertTrue(isinstance(q, dict))


    def test_Methodheap_Frontend_001_getScreenShot_01(self):
        """Test 'getScreenShot' methods from MythTV.Frontend().
        """
        screenshot = self.fe.getScreenShot()
        #print(type(screenshot))
        with open('/tmp/screenshot', 'wb') as f:
            f.write(screenshot)
        os.system('file /tmp/screenshot > /tmp/my_logfile')
        a = ( len(tailandgrep('/tmp/my_logfile', 2, 'JPEG|PNG')) > 0)
        self.assertTrue(a)


if __name__ == '__main__':
    unittest.main()
