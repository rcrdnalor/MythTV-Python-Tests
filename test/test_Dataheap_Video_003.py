# -*- coding: utf-8 -*-

import unittest
import os

from MythTV import MythDB, Video, VideoMetadata

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}


def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Video_003(unittest.TestCase):
    """Test class 'Videos' from dataheap.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        with add_log_flags():
            self.mydb = MythDB()

    def test_Dataheap_Video_003_fromFilename_01(self):
        """Test 'fromFilename' classmethod from MythTV.Video.
           According wiki, this
           "Creates a new object with initial data parsed from the filename.
           Object is not stored to the database."
           Remark: What to do with this 'new object' ?
        """
        path = self.testenv['VIDPATH_DE']
        cast = self.testenv['VIDCAST_DE']

        vid = Video.fromFilename(os.path.basename(path), db=self.mydb)
        self.assertEqual(os.path.basename(path), vid.filename)


    def test_Dataheap_Video_003_exportMetadata_01(self):
        """Test 'exportMetadata' method from MythTV.Video.
        """
        path  = self.testenv['VIDPATH_DE']
        cast  = self.testenv['VIDCAST_DE']
        title = self.testenv['VIDTITLE_DE']

        vids = self.mydb.searchVideos( title = title
                                     , cast  = cast
                                     )
        vid = next(vids)
        self.assertEqual(path, vid.filename)
        # get the metadata of the video
        mtdata = vid.exportMetadata()
        self.assertTrue(isinstance(mtdata, VideoMetadata))
        # save year of video for later use
        year_saved = mtdata.year
        # python 3 does not have a 'long' type
        self.assertTrue((isinstance(year_saved, int)) or (isinstance(year_saved, long)))
        # increment year
        mtdata.year = year_saved + 1
        # write back metadata, allow overwriting existing values
        vid.importMetadata(mtdata, overwrite=True)
        # check year
        self.assertEqual(vid.year, year_saved + 1)
        # restore old year
        vid.year = year_saved
        vid.update()
        # check again year
        mtnew = vid.exportMetadata()
        self.assertEqual(mtnew.year, year_saved)


    def test_Dataheap_Video_003_importMetadata_01(self):
        """Test 'exportMetadata' method from MythTV.Video.
        """
        path  = self.testenv['VIDPATH_DE']
        cast  = self.testenv['VIDCAST_DE']
        title = self.testenv['VIDTITLE_DE']

        vids = self.mydb.searchVideos( title = title
                                     , cast  = cast
                                     )
        vid = next(vids)
        self.assertEqual(path, vid.filename)
        # get the metadata of the video
        mtdata = vid.exportMetadata()
        self.assertTrue(isinstance(mtdata, VideoMetadata))
        ### print(mtdata.keys())
        # save plot of video for later use
        # Note: VideoMetadata.description gets translated to Video.plot
        plot_saved = mtdata.description
        # alter plot
        mtdata.description = mtdata.description + u"test_Dataheap_Video_003_importMetadata_01"
        # write back metadata, allow overwriting existing values
        vid.importMetadata(mtdata, overwrite=True)
        # check plotr
        self.assertEqual(vid.plot, mtdata.description)
        # restore old plot
        vid.plot = plot_saved
        vid.update()
        # check again plot
        mtnew = vid.exportMetadata()
        self.assertEqual(mtnew.description, plot_saved)

if __name__ == '__main__':
    unittest.main()
