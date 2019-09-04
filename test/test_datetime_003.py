# -*- coding: utf-8 -*-

import unittest
import sys
import os

from MythTV.utility.dt import *
from MythTV.utility.singleton import InputSingleton

class test_datetime_003(unittest.TestCase):
    """Test if class 'posixtzinfo' is an 'InputSingleton' of MythTV.utilities.dt."""

    def test_datetime_003_01(self):
        """Test if class 'posixtzinfo' is an 'InputSingleton'.
           MythTV is using metaclasses for getting the time zone info
           in utility/dt.py: The `class posixtzinfo` is designed as
           `InputSingleton`, which means that every subsequent call
           with the same parameter returns the same object. This is
            implemented with the metaclass named 'InputSingleton'.
        """

        a = posixtzinfo()
        b=  posixtzinfo('Etc/UTC')
        c = posixtzinfo("America/Anchorage")

        x = posixtzinfo()
        y = posixtzinfo('Etc/UTC')
        z = posixtzinfo("America/Anchorage")

        self.assertIsNotNone(c)
        self.assertTrue('posixtzinfo' in repr(c))

        # InputSingleton use exactly the same object when called several times
        self.assertEqual(a,x)
        self.assertEqual(b,y)
        self.assertEqual(c,z)


if __name__ == '__main__':
    unittest.main()

