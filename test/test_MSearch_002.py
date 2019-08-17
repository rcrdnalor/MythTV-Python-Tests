# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout
import sys
import os

from MythTV import MSearch

from test.helpers import tailandgrep, add_log_flags


class test_MSearch_002(unittest.TestCase):
    """Test logging of search methodes from MythTV.MSearch."""

    def test_MSearch_002_01(self):
        """Test MSearch.search() logging."""
        a = False ; b = False; c = False
        with add_log_flags():
            m_instance  = MSearch()
            g_generator = m_instance.search()
            u_dict = next(g_generator)
            self.assertTrue('location' in u_dict)
            self.assertIsNotNone(u_dict['location'])
            a = ( len(tailandgrep('/tmp/my_logfile', 3, r'Port 1900 opened for UPnP search')) > 0)
            b = ( len(tailandgrep('/tmp/my_logfile', 4, r'running UPnP search')) > 0 )
            c = ( len(tailandgrep('/tmp/my_logfile', 6, u_dict['st'])) > 0 )
        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)


    def test_MSearch_002_02(self):
        """Test MSearch.searchMythBE() logging."""
        a = False
        with add_log_flags():
            m_instance  = MSearch()
            g_generator = m_instance.searchMythBE()
            u_dict = next(g_generator)
            self.assertTrue('location' in u_dict)
            self.assertIsNotNone(u_dict['location'])
            self.assertTrue('MediaServer'in u_dict['st'])
            a = ( len(tailandgrep('/tmp/my_logfile', 1, u_dict['st'])) > 0 )
        self.assertTrue(a)


    def test_MSearch_002_03(self):
        """Test MSearch.searchMythFE() logging."""
        a = False
        with add_log_flags():
            m_instance  = MSearch()
            g_generator = m_instance.searchMythFE()
            u_dict = next(g_generator)
            self.assertTrue('location' in u_dict)
            self.assertIsNotNone(u_dict['location'])
            self.assertTrue('MediaRenderer'in u_dict['st'])
            a = ( len(tailandgrep('/tmp/my_logfile', 1, u_dict['st'])) > 0 )
        self.assertTrue(a)


    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')


if __name__ == '__main__':
    unittest.main()
