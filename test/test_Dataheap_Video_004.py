# -*- coding: UTF-8 -*-


import unittest

import os

from MythTV import MythDB, Video, DBDataWrite

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)

class test_Dataheap_Video_004(unittest.TestCase):
    """Test creation of a Video and
       writing/reading to the videocategory table.
       This test uses hardcoded values from the file '.testenv'.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        with add_log_flags():
            self.mydb = MythDB()

    def tearDown(self):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')


    def test_Dataheap_Video_004_01(self):
        """Test creation of a Video and
           writing/reading to the videocategory table.
           This test assumes, that there are no entries
           in the videocategory table! All entries in that
           table will be deleted!
        """

        class VideoCategory(DBDataWrite):
            """
            VideoCategory(data=None, db=None) --> VideoCategory object to
            database table 'videocategory', data is a `videocategory` string.

            - get information about the table:
              $ mysql -h <master-backend-ip> -u mythtv -p<password-from-config.xml> mythconverg

              MariaDB [mythconverg]> describe videocategory;
                +-------------+-------------+------+-----+---------+----------------+
                | Field       | Type        | Null | Key | Default | Extra          |
                +-------------+-------------+------+-----+---------+----------------+
                | intid       | int(10)     | NO   | PRI | NULL    | auto_increment |
                | category    | varchar(128)| NO   |     |         |                |
                +-------------+-------------+------+-----+---------+----------------+
                2 rows in set (0.00 sec)

            """
            _table = 'videocategory'
            _key   = ['category']
            _defaults = {'category' : ''}

            ### end class VideoCategory


        title    = u"Le Dernier Métro"
        filename = title + u".mkv"

        vid  = Video(db=self.mydb).create ({'title'   : title,
                                            'filename': filename,
                                            'host'    : self.mydb.getMasterBackend()})

        vid.category = u"python_test"
        vid.update()

        # find this video and check it
        vids = self.mydb.searchVideos( title = title )
        vid_r = next(vids)
        # print(vid_r.category)
        self.assertEqual(vid.category, vid_r.category)
        print(repr(vid_r))
        print(str(vid_r))

        # delete the video previously created
        vid.delete()

        # delete the previously assigned category
        vid_category = VideoCategory(u"python_test", db = self.mydb)
        vid_category.delete()

        # Although, everything is deletes, the 'autoincrement' values are still updated...

if __name__ == '__main__':
    unittest.main()
