# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout
import sys

# OptParse is deperecated since python 3.2+
from optparse import OptionParser

from MythTV import MythLog
from MythTV.static import LOGLEVEL, LOGMASK, LOGFACILITY

from test.helpers import tailandgrep, add_log_flags


class test_Logging_OptParse_001(unittest.TestCase):
    """Test OptParse logging from MythTV.MythLog."""

    def test_logging_OptParse_001_01(self):
        """Test if 'OptParse' works with MythLog."""

        m = MythLog('simple_test')

        parser = OptionParser(prog = "simple_test")
        # silence warnings in unittest about missing '-v' option:
        parser.add_option('-v', action='store_true', dest='uv', default=False
                         , help='Use to set verbosity in unittest')
        # Add arbitrary option:
        parser.add_option('--chanid', action='store', type='int', dest='chanid',
                help='Use chanid for manual operation')
        # load MYthTV's extension
        m.loadOptParse(parser)

        opts, args = parser.parse_args()

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
