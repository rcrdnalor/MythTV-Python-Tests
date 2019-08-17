# -*- coding: utf-8 -*-

import unittest
import os

from MythTV import MythDB, Video

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}


def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Video_002(unittest.TestCase):
    """Test class 'Videos' from dataheap.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv


    def setUp(self):
        self.mydb = MythDB()

    def test_Dataheap_Video_002_parseFilename_01(self):
        """Test 'parseFilename' method from MythTV.Video
           according 'https://www.mythtv.org/wiki/MythVideo_File_Parsing'.
        """

        files = [  # (path,                          result: (title,            season, episode, subtitle     ))
                  (u"A Movie Title.mpg",                      (u"A Movie Title",      None, None, None        ))
                , (u"A Movie Title 2019.mpg",                 (u"A Movie Title 2019", None, None, None        ))
                , (u"Title s01e02 Subtitle2.mpg",             (u"Title",               1,    2,   u"Subtitle2"))
                , (u"Title 3x04 Subtitle4.mpg",               (u"Title",               3,    4,   u"Subtitle4"))
                , (u"Title Season 5 Episode 6 Subtitle6.mpg", (u"Title",               5,    6,   u"Subtitle6"))
                , (u"TV/Indiana Jones/Indiana Jones und das Königreich des Kristallschädels.mkv", (u"Indiana Jones und das Königreich des Kristallschädels", None, None, None))
                ]

        v = Video(db=self.mydb)
        for (path, result) in files:
            v.filename = path
            (title, season, episode, subtitle) = v.parseFilename()
            #print(title, season, episode, subtitle)
            self.assertEqual((title, season, episode, subtitle), result)


    def test_Dataheap_Video_002_parseFilename_02(self):
        """Test 'parseFilename' method from MythTV.Video
           according 'https://www.mythtv.org/wiki/MythVideo_File_Parsing'.
        """
        files = [  # (path,                                         result: (title, season, episode, subtitle ))
                  (u"A_Title/Season 1/02 Subtitle1.mpg",                     (u"A Title",   1,   2, u"Subtitle1" ))
                , (u"B_Title/Season 3/s03e04 Subtitle2.mpg",                 (u"B Title",   3,   4, u"Subtitle2" ))
                , (u"C_Title/Season 5/5x06 Subtitle3.mpg",                   (u"C Title",   5,   6, u"Subtitle3" ))
                , (u"D_Title/Season 7/D Title s07e08 Subtitle4.mpg",         (u"D Title",   7,   8, u"Subtitle4" ))
                , (u"E Title/Season 9/E Title 9x10 Subtitle5.mpg",           (u"E Title",   9,  10, u"Subtitle5" ))
                , (u"F Title/Season 11/Episode 12 Subtitle6.mpg",            (u"F Title",  11,  12, u"Subtitle6" ))
                , (u"G Title/Season 13/Season 13 Episode 14 Subtitle7.mpg",  (u"G Title",  13,  14, u"Subtitle7" ))
                , (u"H Title Season 15/16 Subtitle8.mpg",                    (u"H Title",  15,  16, u"Subtitle8" ))
                , (u"I_Title Season 17/s17e18 Subtitle9.mpg",                (u"I Title",  17,  18, u"Subtitle9" ))
                , (u"J_Title Season 19/19x20 Subtitle10.mpg",                (u"J Title",  19,  20, u"Subtitle10"))
                , (u"K_Title Season 21/K Title s21e22 Subtitle11.mpg",       (u"K Title",  21,  22, u"Subtitle11"))
                , (u"L_Title Season 23/L Title 23x024 Subtitle12.mpg",       (u"L Title",  23,  24, u"Subtitle12"))
                , (u"M_Title Season 25/Episode 26 Subtitle13.avi",           (u"M Title",  25,  26, u"Subtitle13"))
                , (u"N_Title Season 27/Season 27 Episode 28 Subtitle14.mkv", (u"N Title",  27,  28, u"Subtitle14"))
                ]
        v = Video(db=self.mydb)
        for (path, result) in files:
            v.filename = path
            (title, season, episode, subtitle) = v.parseFilename()
            #print(title, season, episode, subtitle)
            self.assertEqual((title, season, episode, subtitle), result)

if __name__ == '__main__':
    unittest.main()
