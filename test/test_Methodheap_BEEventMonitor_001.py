# -*- coding: utf-8 -*-

import unittest

from MythTV import BEEventMonitor, Frontend

import time
import os

from test.helpers import tailandgrep, add_log_flags, get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)

class test_Methodheap_BEEventMonitor_001(unittest.TestCase):
    """Test methods from MythTV.BEEventMonitor().
    """
    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        with add_log_flags():
            # connect to frontend and prepare a recording to play
            self.fe = Frontend("%s" %(self.testenv['FRONTENDIP']), 6546)
            self.p  = "%s %s" %(self.testenv['RECCHANID'], self.testenv['RECSTARTTIMEUTC'].strip('Z'))

    def tearDown(self):
        # close frontend
        self.fe.close()

    @classmethod
    def tearDownClass(cls):
        # clear test environment
        global TestEnv
        TestEnv.clear()
        # remove temorary files
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')


    def test_test_Methodheap_BEEventMonitor_001_01(self):
        """Test 'BEEventMonitor' from MythTV.BEEventMonitor() with logging.
           Start the BEEventMonitor and watch the logs for events.
        """
        self.a = 0

        bemon = BEEventMonitor(systemevents=True)
        time.sleep(1)

        # start generating some log messages:
        # Jump to 'TV Recording Playback',
        loc = self.fe.sendQuery('location')
        if (loc != 'playbackbox'):
            self.fe.jump['playbackrecordings']
            time.sleep(1)

        # Select recordings
        k1 = self.fe.key['enter']
        self.assertTrue(k1)
        time.sleep(1)

        # Play program with chanid & starttime
        # play program CHANID yyyy-MM-ddThh:mm:ss
        k2 = self.fe.sendPlay('program %s' %self.p)
        self.assertTrue(k2)
        time.sleep(15)

        # stop playback of recording
        k3 = self.fe.key.escape
        self.assertTrue(k3)
        time.sleep(1)

        a =  tailandgrep( '/tmp/my_logfile', 50
                        , 'BACKEND_MESSAGE\[\]:\[\]SYSTEM_EVENT PLAY_STOPPED HOSTNAME'
                        )

        self.assertTrue((len(a) > 0))


if __name__ == '__main__':
    unittest.main()
