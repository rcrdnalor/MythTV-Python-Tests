# -*- coding: utf-8 -*-

import unittest
import re
from sys import stdout
import sys
import os

# OptParse is deperecated since python 3.2+
from optparse import OptionParser

from MythTV import MythLog
from MythTV.static import LOGLEVEL, LOGMASK, LOGFACILITY

from test.helpers import tailandgrep, add_log_flags


class test_Logging_OptParse_002(unittest.TestCase):
    """Test OptParse logging from MythTV.MythLog."""

    def test_logging_OptParse_002_01(self):
        """Test if 'OptParse' works with MythLog."""

        # set default values acc. source code
        m_dblog    = True
        m_loglevel = LOGLEVEL.INFO
        m_verbose  = LOGMASK.GENERAL
        m_logfile  = stdout

        with add_log_flags():
            m = MythLog('simple_test')

            #print ("m._LEVEL = %d" %m._LEVEL)
            #print ("m._MASK  = %d" %m._MASK)
            #print ("m._DBLOG = %s" %m._DBLOG)
            #print sys.argv
            parser = OptionParser(prog = "simple_test")

            # silence warnings in unittest about missing '-v' option:
            parser.add_option('-v', action='store_true', dest='uv', default=False
                              , help='Use to set verbosity in unittest')

            # load MYthTV's extension
            m.loadOptParse(parser)
            opts, args = parser.parse_args()

            # check the options provided by 'additional_args':
            m_dblog    = opts.dblog    # the options is named '--nodblog', but stored in 'dblog'
            m_loglevel = m._LEVEL
            m_verbose  = m._MASK
            m_logfile  = m._LOGFILE

        self.assertEqual(m_dblog, True)
        self.assertEqual(m_loglevel, LOGLEVEL.DEBUG)
        self.assertEqual(m_verbose,LOGMASK.ALL)      ### XXX RER '-v' from unittest collides with this
        self.assertTrue(os.path.exists("/tmp/my_logfile"))



if __name__ == '__main__':
    unittest.main()
