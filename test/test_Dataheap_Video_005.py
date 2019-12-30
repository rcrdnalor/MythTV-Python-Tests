# -*- coding: UTF-8 -*-


import unittest

import os
import subprocess

from MythTV import MythDB, Video, DBDataWrite

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Video_005(unittest.TestCase):
    """Test creation of a Video with an existing file and host entry.
       This test uses hardcoded values from the file '.testenv'.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        # create a file with this name if it does not exist
        self.frtitle    = self.testenv["VIDFRTITLE"]    # Le Dernier Métro"
        self.frfilename = self.testenv["VIDFRFILENAME"]
        self.frpath     = self.testenv["VIDFRPATH"]
        self.frfullpath = os.path.join(self.frpath, self.frfilename)
        with add_log_flags():
            self.mydb = MythDB()
        self.master_backend_ip = self.mydb.settings['NULL']['MasterServerIP']
        shcmd = 'head -c 10M </dev/urandom > "%s"' %self.frfullpath
        cmd = "ssh mythtv@%s '%s'" %(self.master_backend_ip, shcmd)
        print(cmd)
        self.result = subprocess.call(cmd, shell=True)  # will be checked later

    def tearDown(self):
        # remove log file
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')
        # remove temporary video file
        shcmd = 'rm "%s"' %self.frfullpath
        cmd = "ssh mythtv@%s '%s'" %(self.master_backend_ip, shcmd)
        print(cmd)
        subprocess.call(cmd, shell=True)


    def test_Dataheap_Video_005_01(self):
        """Test creation of a Video with an existing file and host entry.
        """

        # check the result of the file creation
        self.assertTrue(self.result == 0)

        host = self.mydb.getMasterBackend()

        v = Video(db=self.mydb)
        v.host = host
        v.filename = self.frfilename
        v.create({'title': self.frtitle, 'filename': self.frfilename, 'host': host})

        # check if hash is in hex:
        hex_set = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}
        self.assertTrue(set(v.hash.lower()).issubset(hex_set))

        #remove video entry
        v.delete()

if __name__ == '__main__':
    unittest.main()
