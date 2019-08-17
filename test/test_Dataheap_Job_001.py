# -*- coding: utf-8 -*-

import unittest
import os
import time
import re
#import copy
from pprint import pprint

from MythTV import MythDB, Recorded, Program, Job, MythError

from MythTV.static  import JOBTYPE, JOBSTATUS, JOBFLAG, RECSTATUS

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Job_001(unittest.TestCase):
    """Test class 'Job 'dataheap'.
       This test uses hardcoded values from the file '.testenv'.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        with add_log_flags():
            self.mydb = MythDB()

    def tearDown(self):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

    def test_Dataheap_Job_001_01(self):
        """Test classmethod Job.fromRecorded() from 'dataheap'.
        This test triggers a job to rebuild the the seek table of a recording.
        Note: I did not realized that this is possible, it is not mentioned
        in the wiki. You have to grep the source code for the flag 'JOB_REBUILD'.
        Additional note: The log does not say anything about rebuilding the seektable.
        """
        chanid        = self.testenv['DOWNCHANID']
        starttimemyth = self.testenv['DOWNSTARTTIME']

        hostname = self.mydb.getMasterBackend()
        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        myjob = Job.fromRecorded(rec, JOBTYPE.COMMFLAG, hostname=hostname,
                                 flags=JOBFLAG.REBUILD)

        loopnr = 0
        while (myjob.status < JOBSTATUS.FINISHED):
            time.sleep(10)
            myjob._pull()     # this re-reads the jobqueue table
            loopnr += 1
            if (loopnr > 60):
                break

        self.assertEqual(myjob.status, JOBSTATUS.FINISHED)


if __name__ == '__main__':
    unittest.main()
