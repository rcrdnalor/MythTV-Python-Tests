# -*- coding: utf-8 -*-

import unittest
import os

from MythTV import MythDB, RecordedArtwork, Video

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}


def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Video_001(unittest.TestCase):
    """Test class 'Videos' from dataheap.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv


    def setUp(self):
        self.mydb = MythDB()

    def test_Dataheap_Video_001_getHash_01(self):
        """Test 'getHash' method from MythTV.Video
           using 'searchVideos'.
        """

        vids = self.mydb.searchVideos( title = self.testenv['VIDTITLE']
                                     , cast  = self.testenv['VIDCAST']
                                     )
        vid = next(vids)
        #print("%s : %s" %(vid.title, type(vid.title)))
        self.assertTrue(isinstance(vid, Video))
        vid_hash = vid.getHash()
        # check if retval is hexadecimal:
        hex_set = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}
        self.assertTrue(set(vid_hash.lower()).issubset(hex_set))

        # test '__repr__' and '__str__'
        print()
        print(repr(vid))
        print(str(vid))

if __name__ == '__main__':
    unittest.main()
