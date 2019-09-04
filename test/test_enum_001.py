# -*- coding: utf-8 -*-

import unittest


from MythTV import EnumValue, Enum, BitwiseEnum


class test_Enum_001(unittest.TestCase):
    """Test 'Enum' methodes from MythTV.utility.enum."""

    def test_Enum_001_01(self):
        """Test MythTV.utility.Enum."""

        global count_1
        count_1 = 0

        class enum_01(Enum):
            UNKNOWN      = 0x0000
            QUEUED       = 0x0001
            PENDING      = 0x0002
            STARTING     = 0x0003
            RUNNING      = 0x0004

        my_e0 = enum_01.UNKNOWN
        my_e3_value = enum_01.STARTING
        my_e4 = enum_01.RUNNING
        my_e4_str = str(enum_01(4))

        self.assertEqual(int(my_e4), 4)

        # test 'str' and 'repr', too:
        self.assertEqual(str(my_e0), 'UNKNOWN')
        self.assertEqual(repr(my_e0), "<enum_01 'UNKNOWN'>")
        self.assertEqual(str(my_e3_value), 'STARTING')
        self.assertEqual(str(enum_01(4)), 'RUNNING')
        self.assertEqual(my_e4_str, 'RUNNING')
        self.assertEqual(repr(my_e4), "<enum_01 'RUNNING'>")


class test_Enum_002(unittest.TestCase):
    """Test 'BitwiseEnum' methodes from MythTV.utility.enum."""

    def test_Enum_002_01(self):
        """Test MythTV.utility.BitwiseEnum."""

        global count_1
        count_1 = 0

        class enum_02(BitwiseEnum):
            NONE        = 0b000000000000000000000000000
            GENERAL     = 0b000000000000000000000000001
            RECORD      = 0b000000000000000000000000010
            PLAYBACK    = 0b000000000000000000000000100
            CHANNEL     = 0b000000000000000000000001000

        my_e0 = enum_02.NONE
        my_e3_value = enum_02.PLAYBACK
        my_e4 = enum_02.CHANNEL
        my_e4_str = str(enum_02(4))

        self.assertEqual(int(enum_02.CHANNEL | enum_02.PLAYBACK), 0b1100)
        self.assertEqual(int(enum_02.CHANNEL ^ enum_02.CHANNEL), 0)

        # test 'str' and 'repr', too:
        self.assertEqual(str(my_e0), 'NONE')
        self.assertEqual(repr(my_e0), "<enum_02 NONE>")
        self.assertEqual(str(my_e3_value), 'PLAYBACK')
        self.assertEqual(str(enum_02(4)), 'PLAYBACK')
        self.assertEqual(my_e4_str, 'PLAYBACK')
        self.assertEqual(repr(my_e4), "<enum_02 CHANNEL>")


if __name__ == '__main__':
    unittest.main()
