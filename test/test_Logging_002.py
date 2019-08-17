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


class test_Logging_Basic_003(unittest.TestCase):
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

    def test_Logging_Basic_003_01(self):
        """Test that default options does not work without a MythLog instance."""

        with self.assertRaises(AttributeError):
            # check the default mask:
            self.assertEqual(MythLog._MASK, LOGMASK.GENERAL)

        with self.assertRaises(AttributeError):
            # check the default level:
            self.assertEqual(MythLog._LEVEL, LOGLEVEL.INFO)

        with self.assertRaises(AttributeError):
            # check the default file:
            self.assertTrue('stdout' in repr(MythLog._LOGFILE))


class test_Logging_Basic_004(unittest.TestCase):
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

    def test_Logging_Basic_004_01(self):
        """"Test if setting options works without a MythLog instance."""

        MythLog._setmask("most")
        # check the modified mask:
        self.assertEqual(MythLog._MASK, LOGMASK.MOST)
        # check the default level:
        self.assertEqual(MythLog._LEVEL, LOGLEVEL.INFO)
        # check the default file:
        self.assertTrue('stdout' in repr(MythLog._LOGFILE))

        MythLog._setlevel("notice")
        # check the modified mask:
        self.assertEqual(MythLog._MASK, LOGMASK.MOST)
        # check the modified level:
        self.assertEqual(MythLog._LEVEL, LOGLEVEL.NOTICE)
        # check the default file:
        self.assertTrue('stdout' in repr(MythLog._LOGFILE))

        MythLog._setfile("/tmp/my_logfile")
        # check the modified mask:
        self.assertEqual(MythLog._MASK, LOGMASK.MOST)
        # check the modified level:
        self.assertEqual(MythLog._LEVEL, LOGLEVEL.NOTICE)
        # check the modified file:
        self.assertTrue(os.path.exists("/tmp/my_logfile"))

if __name__ == '__main__':
    if os.path.exists('/tmp/my_logfile'):
        os.remove('/tmp/my_logfile')
    unittest.main()
