# -*- coding: utf-8 -*-

import unittest

from MythTV import Singleton, InputSingleton, CmpSingleton
from future.utils import with_metaclass


class test_Singleton_001(unittest.TestCase):
    """Test 'singelton' methodes from MythTV.utility.singleton."""

    def test_Singleton_001_01(self):
        """Test MythTV.utility.Singleton."""

        global count_1
        count_1 = 0

        class foo_01(with_metaclass(Singleton, object)):
            def __init__(self):
                global count_1
                self._count = count_1
                self._count += 1
                count_1 = self._count

        a = foo_01()
        b = foo_01()
        c = foo_01()

        #print(count_1)
        self.assertEqual(repr(a), repr(b))
        self.assertEqual(count_1 , 1)

    def test_Singleton_002_01(self):
        """Test MythTV.utility.InputSingleton."""

        global count_2
        count_2 = 0

        class foo_02(with_metaclass(InputSingleton, object)):
            def __init__(self, fooname = None):
                global count_2
                self._count = count_2
                self._count += 1
                count_2 = self._count
                self.fooname = fooname

        a = foo_02("x")
        b = foo_02("y")
        c = foo_02()
        d = foo_02("x")
        e = foo_02()

        #print(count_2)
        self.assertEqual(repr(a), repr(d))
        self.assertEqual(repr(c), repr(e))
        self.assertEqual(count_2 , 3)


if __name__ == '__main__':
    unittest.main()
