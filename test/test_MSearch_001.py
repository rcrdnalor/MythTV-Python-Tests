# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout
import sys

from MythTV import MSearch


class test_MSearch_001(unittest.TestCase):
    """Test search methodes from MythTV.MSearch."""

    def test_MSearch_001_01(self):
        """Test MSearch.search()."""
        m_instance  = MSearch()
        g_generator = m_instance.search()
        u_dict = next(g_generator)
        self.assertTrue('location' in u_dict)
        self.assertIsNotNone(u_dict['location'])


    def test_MSearch_001_02(self):
        """Test MSearch.searchMythBE()."""
        m_instance  = MSearch()
        g_generator = m_instance.searchMythBE()
        u_dict = next(g_generator)
        self.assertTrue('location' in u_dict)
        self.assertIsNotNone(u_dict['location'])
        self.assertTrue('MediaServer'in u_dict['st'])


    def test_MSearch_001_03(self):
        """Test MSearch.searchMythFE()."""
        m_instance  = MSearch()
        g_generator = m_instance.searchMythFE()
        u_dict = next(g_generator)
        self.assertTrue('location' in u_dict)
        self.assertIsNotNone(u_dict['location'])
        self.assertTrue('MediaRenderer'in u_dict['st'])


if __name__ == '__main__':
    unittest.main()
