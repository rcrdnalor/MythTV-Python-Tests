# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout
import sys
import os

# OptParse is deperecated since python 3.2+
from optparse import OptionParser

import MythTV
from MythTV import MythLog
from MythTV.static import LOGLEVEL, LOGMASK, LOGFACILITY

from test.helpers import tailandgrep, add_log_flags


class test_Logging_Basic_001(unittest.TestCase):
    """Test basic logging from MythTV.MythLog."""

    def setUp(self):
        try:
            reload(MythTV)
        except:
            import importlib
            importlib.reload(MythTV)
        from MythTV import MythLog

    def tearDown(self):
        try:
            reload(MythTV)
        except:
            import importlib
            importlib.reload(MythTV)
        from MythTV import MythLog

    def test_Logging_Basic_001_01(self):
        """Test if default options works with MythLog."""

        m = MythLog('simple_test')

        # check the default mask:
        self.assertEqual(m._MASK, LOGMASK.GENERAL)
        # check the default level:
        self.assertEqual(m._LEVEL, LOGLEVEL.INFO)
        # check the default file:
        self.assertTrue('stdout' in repr(m._LOGFILE))

        # test '__repr__' and '__str__'
        print()
        print(repr(m))
        print(str(m))



class test_Logging_Basic_002(unittest.TestCase):
    """Test if options can be modified from MythTV.MythLog."""

    def setUp(self):
        try:
            reload(MythTV)
        except:
            import importlib
            importlib.reload(MythTV)
        from MythTV import MythLog
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

    def tearDown(self):
        try:
            reload(MythTV)
        except:
            import importlib
            importlib.reload(MythTV)
        from MythTV import MythLog
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

    def test_Logging_Basic_002_01(self):
        """Test if options can be modified from MythTV.MythLog."""

        m = MythLog('simple_test')

        m._setmask("most")
        # check the modified mask:
        self.assertEqual(m._MASK, LOGMASK.MOST)
        # check the default level:
        self.assertEqual(m._LEVEL, LOGLEVEL.INFO)
        # check the default file:
        self.assertTrue('stdout' in repr(m._LOGFILE))

        m._setlevel("notice")
        # check the modified mask:
        self.assertEqual(m._MASK, LOGMASK.MOST)
        # check the modified level:
        self.assertEqual(m._LEVEL, LOGLEVEL.NOTICE)
        # check the default file:
        self.assertTrue('stdout' in repr(m._LOGFILE))

        m._setfile("/tmp/my_logfile")
        # check the modified mask:
        self.assertEqual(m._MASK, LOGMASK.MOST)
        # check the modified level:
        self.assertEqual(m._LEVEL, LOGLEVEL.NOTICE)
        # check the modified file:
        self.assertTrue(os.path.exists("/tmp/my_logfile"))

if __name__ == '__main__':
    if os.path.exists('/tmp/my_logfile'):
        os.remove('/tmp/my_logfile')
    unittest.main()
