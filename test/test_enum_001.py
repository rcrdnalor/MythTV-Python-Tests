# -*- coding: utf-8 -*-

import unittest


from MythTV import Enum, BitwiseEnum


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

        my_enum_04_val = enum_01(4)
        self.assertEqual(str(my_enum_04_val), 'RUNNING')
        self.assertEqual(int(my_enum_04_val), 4)

        self.assertTrue(int(my_e3_value) < int(my_e4))             # True
        self.assertTrue(int(my_e3_value) < my_e4)                  # True
        self.assertTrue(my_e3_value < my_e4)                       # True
        self.assertFalse(my_e3_value > my_e4)                       # False
        self.assertTrue(my_e3_value != my_e4)
        self.assertTrue(enum_01(2) == enum_01.PENDING)             # True
        self.assertTrue(enum_01(2) <= enum_01.PENDING)             # True 
        self.assertTrue(enum_01(2) >= enum_01.PENDING)             # True 

        with self.assertRaises(AttributeError) as context:
            my_e5_value = str(enum_01.STOPPING)
        self.assertTrue('STOPPING' in str(context.exception))


    def test_Enum_001_02(self):
        """Test MythTV.utility.Enum."""

        global count_1
        count_1 = 1

        class enum_03(Enum):
            UNKNOWN      = 0x0000
            QUEUED       = 0x0001
            PENDING      = 0x0002
            STARTING     = 0x0003
            RUNNING      = 0x0004
            STARTING1    = 0x0003
            
        self.assertTrue(enum_03.STARTING == enum_03.STARTING1)   


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
        my_e5 = enum_02.CHANNEL
        my_e5 |= enum_02.PLAYBACK
        self.assertEqual(my_e5, 0b1100)
        a = enum_02.RECORD.__ror__(enum_02.GENERAL)
        self.assertEqual(a, 3)
        
        b = enum_02.CHANNEL | enum_02.PLAYBACK
        b = b & enum_02.PLAYBACK
        self.assertTrue(b, 0b100)
        
        c = enum_02.CHANNEL | enum_02.PLAYBACK
        c &= enum_02.PLAYBACK
        self.assertTrue(b, 0b100)
        d = enum_02.RECORD.__rand__(enum_02.GENERAL)
        self.assertEqual(d, 0)
        
        self.assertEqual(int(enum_02.CHANNEL ^ enum_02.CHANNEL), 0)
        my_e6 = enum_02.CHANNEL
        my_e6 ^= enum_02.PLAYBACK
        self.assertEqual(my_e6, 0b1100)
        e = my_e6.__rxor__(enum_02.GENERAL)
        self.assertEqual(e, 0b1101)

        # test 'str' and 'repr', too:
        self.assertEqual(str(my_e0), 'NONE')
        self.assertEqual(repr(my_e0), "<enum_02 NONE>")
        self.assertEqual(str(my_e3_value), 'PLAYBACK')
        self.assertEqual(str(enum_02(4)), 'PLAYBACK')
        self.assertEqual(my_e4_str, 'PLAYBACK')
        self.assertEqual(repr(my_e4), "<enum_02 CHANNEL>")


    def test_Enum_002_02(self):
        """Test MythTV.utility.BitwiseEnum."""

        global count_1
        count_1 = 1

        class enum_04(BitwiseEnum):
            NONE        = 0b000000000000000000000000000
            GENERAL     = 0b000000000000000000000000001
            RECORD      = 0b000000000000000000000000010
            PLAYBACK    = 0b000000000000000000000000100
            CHANNEL     = 0b000000000000000000000001000
            RECORD1     = 0b000000000000000000000000010
            
        #print( repr( enum_04 ))
        self.assertTrue(enum_04.RECORD == enum_04.RECORD1)    


if __name__ == '__main__':
    unittest.main()
