# -*- coding: utf-8 -*-

import unittest
import re
import os
from sys import stdout, argv

import argparse

from MythTV import MythLog
from MythTV.static import LOGLEVEL, LOGMASK, LOGFACILITY

from test.helpers import tailandgrep, add_log_flags


class test_Logging_argparse_002(unittest.TestCase):
    """Test argparse logging from MythTV.MythLog."""

    def test_Logging_argparse_002_01(self):
        """Test if 'argparse' works with MythLog."""

        # set default values acc. source code
        m_dblog    = True
        m_loglevel = LOGLEVEL.INFO
        m_verbose  = LOGMASK.GENERAL
        m_logfile  = stdout

        with add_log_flags():
            m = MythLog('simple_test')
            parser = argparse.ArgumentParser(prog = "simple_test")

            # load MYthTV's extension
            m.loadArgParse(parser)

            # unittest : first arguements are the test class or the verbosity flag
            # filter out arguements for unittesting:
            test_args = add_log_flags.additional_args

            # according 'add_log_flags', test_args should be:
            #  ['--nodblog', '--loglevel', 'debug', '--verbose', 'all', '--logfile', '/tmp/my_logfile']

            args = parser.parse_args(test_args)
            #print(test_args)
            #print(args)

            # check the options provided by 'additional_args':
            m_dblog    = m._DBLOG
            m_loglevel = m._LEVEL
            m_verbose  = m._MASK
            m_logfile  = m._LOGFILE

        self.assertEqual(m_dblog, False)
        self.assertEqual(m_loglevel, LOGLEVEL.DEBUG)
        self.assertEqual(m_verbose,LOGMASK.ALL)
        self.assertTrue(os.path.exists("/tmp/my_logfile"))

    def tearDown(self):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')


if __name__ == '__main__':
    unittest.main()
