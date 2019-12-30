# -*- coding: UTF-8 -*-


import unittest

from MythTV import MythDB
from MythTV.utility import check_ipv6

import re
import os
import sys

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)

class test_DBCache_001(unittest.TestCase):
    """Test settings from class 'DBCache in file 'database.py'.
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


    def test_DBCache_001_01(self):
        """Get all settings from database.
           Create, read, and write a specific setting.
        """

        print("Python-Version: %d" %sys.version_info[0])

        host = self.mydb.getMasterBackend()

        # get all global settings:
        all_glob_settings = self.mydb.settings.NULL.getall()
        ip = 'blah'
        for k,v in list(all_glob_settings):
            if k == u'MasterServerIP':
                ip = v
                break
        #print(ip)   # --> '192.168.47.11'
        ipv4_valid = re.match(r'(?:\d{1,3}\.){3}\d{1,3}', ip)
        ipv6_valid = check_ipv6(ip)
        self.assertTrue(ipv4_valid or ipv6_valid)

        # get all settings from host:
        all_host_settings = self.mydb.settings[host].getall()
        setting_found = False
        for k,v in list(all_host_settings):
            if k == u'DateFormat':
                setting_found = True
                break
        #print(setting_found)
        self.assertTrue(setting_found)

        # create a setting:
        self.mydb.settings[host][u"mailTO"] = u"justme@gmail.at"
        # update a setting:
        self.mydb.settings[host][u"mailTO"] = u"justme@gmail.com"
        mailTo = self.mydb.settings[host][u"mailTO"]
        # check that setting
        self.assertEqual(mailTo, u"justme@gmail.com")

        # delete a setting:
        del self.mydb.settings[host][u"mailTO"]

        #print(self.mydb.settings[host][u"mailTO"])  #   --> None
        self.assertIsNone(self.mydb.settings[host][u"mailTO"])


if __name__ == '__main__':
    unittest.main()
