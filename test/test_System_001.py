# -*- coding: utf-8 -*-

import unittest
import sys
import os
from test.helpers import tailandgrep, add_log_flags

from MythTV import System, MythError, MythFileError, MythLog


class test_System_001(unittest.TestCase):
    """Test basic system calls from MythTV.System."""

    def test_system_001_01(self):
        """Test if 'System' executes 'echo' command."""

        with add_log_flags():
            s = System(path='echo')
            out = s("Hello World!")

        self.assertEqual(out.decode('utf-8'), "Hello World!\n")


    def test_system_001_02(self):
        """Test if 'System' failes on 'exho' command."""

        with add_log_flags():
            with self.assertRaises(MythFileError):
                s = System(path='xcho')
                out = s("Hello World!")


class test_System_002(unittest.TestCase):
    """Test basic system calls from MythTV.System.system."""

    def test_system_002_01(self):
        """Test if 'System.system' executes 'echo' command."""

        a = False
        out = 1
        with add_log_flags():
            out = System.system("echo Hello World!")
            a   = ( len(tailandgrep("/tmp/my_logfile", 4, u"Hello World!")) > 0 )

        self.assertEqual(a, True)
        self.assertEqual(out, 0)


    def test_system_002_02(self):
        """Test if 'System.system' failes on 'exho' command."""

        out = 0
        with add_log_flags():
            out = System.system('exho Hello World!')
            a   = ( len(tailandgrep('/tmp/my_logfile', 4, r'Hello World!')) > 0 )

        self.assertEqual(out, -1)


    def test_system_002_03(self):
        """Test if 'System.system' executes command specified to report to 'stderr'.
        """

        a = False
        out = 1
        with add_log_flags():
            out = System.system('echo Hello Error >&2')
            a   = ( len(tailandgrep('/tmp/my_logfile', 4, r'Hello Error')) > 0 )

        self.assertEqual(a, True)
        self.assertEqual(out, 0)


class test_System_003(unittest.TestCase):
    """Test basic system calls with unicode from MythTV.System.system."""

    def test_system_003_01(self):
        """Test if 'System.system' executes 'echo' command with unicode characters."""

        a = False
        out = None
        with add_log_flags():
            s = System(path='echo')
            out = s(u"Süßes Leben")
            a   = ( len(tailandgrep('/tmp/my_logfile', 4, u'Süßes Leben')) > 0 )
        self.assertEqual(a, True)
        self.assertEqual(out, u"Süßes Leben\n".encode('utf-8'))


    @classmethod
    def tearDownClass(cls):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

if __name__ == '__main__':
    if os.path.exists('/tmp/my_logfile'):
        os.remove('/tmp/my_logfile')
    unittest.main()

