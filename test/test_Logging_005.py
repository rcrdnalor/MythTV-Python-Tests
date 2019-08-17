# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout, argv

import argparse

from MythTV import MythLog
from MythTV.static import LOGLEVEL, LOGMASK, LOGFACILITY

from test.helpers import tailandgrep, add_log_flags


class test_Logging_argparse_001(unittest.TestCase):
    """Test argparse logging from MythTV.MythLog."""

    def test_Logging_argparse_001_01(self):
        """Test if 'argparse' works with MythLog."""

        m = MythLog('simple_test')

        parser = argparse.ArgumentParser(prog = "simple_test")

        # Add arbitrary option:
        parser.add_argument('--chanid', action='store', dest='chanid', default=0
                           , help='Use chanid for manual operation')

        # load MYthTV's extension
        m.loadArgParse(parser)

        # unittest : first arguements are the test class or the verbosity flag
        test_args = []
        args_found = False
        for a in argv:
            if not args_found:
                args_found = a.startswith('test')
            else:
                test_args.append(a)

        args = parser.parse_args(test_args)

        # check the default mask:
        self.assertEqual(m._MASK, LOGMASK.GENERAL)

        # check if helptext contains 'siparser'
        h = m.helptext
        found = False
        for line in h.split("\n"):
            match = re.findall(r'siparser', line)
            if match:
                found = True
        self.assertEqual(found, True)



if __name__ == '__main__':
    unittest.main()
