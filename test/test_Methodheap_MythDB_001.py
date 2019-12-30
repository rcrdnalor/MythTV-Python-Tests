# -*- coding: utf-8 -*-

import unittest

from MythTV import MythDB, Recorded, OldRecorded, RecordedArtwork, Job, Guide, Record, Video, MythFEError, datetime

from test.helpers import get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)



class test_Methodheap_MythDB_001(unittest.TestCase):
    """Test method 'searchRecorded' from MythTV.MythDB().
       This test uses hardcoded values from the file '.testenv'.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_001_searchRecorded_01(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'chanid'.
        """

        recs =  self.mydb.searchRecorded(chanid = self.testenv['RECCHANID'])
        rec01 = next(recs)
        self.assertTrue(isinstance(rec01, Recorded))


    def test_Methodheap_MythDB_001_searchRecorded_02(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'chanid', 'title'.
        """

        recs =  self.mydb.searchRecorded( chanid = self.testenv['RECCHANID']
                                        , title  = self.testenv['RECTITLE']
                                        )
        rec01 = next(recs)
        self.assertTrue(isinstance(rec01, Recorded))
        # check if accessing a property works
        self.assertTrue(rec01.basename == self.testenv['RECBASENAME'])


    def test_Methodheap_MythDB_001_searchRecorded_03(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'newerthan'.
        """

        # substract 1 minute from starttime
        starttime_before = int(self.testenv['RECSTARTTIMEMYTH']) - 100
        recs =  self.mydb.searchRecorded( chanid = self.testenv['RECCHANID']
                                        , newerthan = starttime_before
                                        )
        rec01 = next(recs)
        self.assertTrue(isinstance(rec01, Recorded))
        # check if accessing a property works
        self.assertTrue(rec01.basename == self.testenv['RECBASENAME'])


    def test_Methodheap_MythDB_001_searchRecorded_04(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'olderthan' and 'newerthan'.
        Time is given in 'mythtime' notation.
        """

        # substract / add 1 minute from/to starttime
        starttime_before = int(self.testenv['RECSTARTTIMEMYTH']) - 100
        starttime_after  = int(self.testenv['RECSTARTTIMEMYTH']) + 100
        recs =  self.mydb.searchRecorded( chanid = self.testenv['RECCHANID']
                                        , olderthan = starttime_after
                                        , newerthan = starttime_before
                                        )
        rec01 = next(recs)
        self.assertTrue(isinstance(rec01, Recorded))
        # check if accessing a property works
        self.assertTrue(rec01.basename == self.testenv['RECBASENAME'])


    def test_Methodheap_MythDB_001_searchRecorded_05(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'olderthan' and 'newerthan'.
           Time values are passed in UTC and ISO format.
        """

        # substract / add 1 minute from/to starttime
        starttime_before = int(self.testenv['RECSTARTTIMEMYTH']) - 100
        starttime_after  = int(self.testenv['RECSTARTTIMEMYTH']) + 100

        # transform to utc iso, like '2019-03-05T12:50:00Z'
        starttime_before_utc_iso = datetime.duck(starttime_before).utcisoformat() +"Z"
        starttime_after_utc_iso  = datetime.duck(starttime_after).utcisoformat() +"Z"

        recs =  self.mydb.searchRecorded( chanid = self.testenv['RECCHANID']
                                        , olderthan = starttime_after_utc_iso
                                        , newerthan = starttime_before_utc_iso
                                        )
        rec01 = next(recs)

        self.assertTrue(isinstance(rec01, Recorded))
        # check if accessing a property works
        self.assertTrue(rec01.basename == self.testenv['RECBASENAME'])


    def test_Methodheap_MythDB_001_searchRecorded_06(self):
        """Test 'seachRecorded' method from MythTV.MythDB() using 'olderthan',
           'newerthan' and the 'closedcaptioned' property.
           Time values are passed in UTC and ISO format.
        """

        # substract / add 1 minute from/to starttime
        starttime_before = int(self.testenv['RECSTARTTIMEMYTH']) - 100
        starttime_after  = int(self.testenv['RECSTARTTIMEMYTH']) + 100

        # transform to utc iso, like '2019-03-05T12:50:00Z'
        starttime_before_utc_iso = datetime.duck(starttime_before).utcisoformat() +"Z"
        starttime_after_utc_iso  = datetime.duck(starttime_after).utcisoformat() +"Z"

        recs =  self.mydb.searchRecorded( chanid = self.testenv['RECCHANID']
                                        , olderthan = starttime_after_utc_iso
                                        , newerthan = starttime_before_utc_iso
                                        , closecaptioned = 0
                                        )
        rec01 = next(recs)

        self.assertTrue(isinstance(rec01, Recorded))
        # check if accessing a property works
        self.assertTrue(rec01.basename == self.testenv['RECBASENAME'])


class test_Methodheap_MythDB_002(unittest.TestCase):
    """Test method 'searchOldRecorded' from MythTV.MythDB()."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_002_searchOldRecorded_01(self):
        """Test 'searchOldRecorded' method from MythTV.MythDB() via 'chanid'.
        """

        recs  =  self.mydb.searchOldRecorded(chanid = self.testenv['RECCHANID'])
        rec02 =  next(recs)
        self.assertTrue(isinstance(rec02, OldRecorded))


    def test_Methodheap_MythDB_002_searchOldRecorded_02(self):
        """Test 'searchOldRecorded' method from MythTV.MythDB() via 'chanid', 'title'.
        """

        recs  =  self.mydb.searchOldRecorded( chanid = self.testenv['RECCHANID']
                                            , title  = self.testenv['RECTITLE']
                                            )
        rec02 =  next(recs)
        self.assertTrue(isinstance(rec02, OldRecorded))
        # check if accessing a property works
        self.assertTrue(rec02.recordid == int(self.testenv['RECRECORDID']))


    def test_Methodheap_MythDB_002_searchOldRecorded_03(self):
        """Test 'searchOldRecorded' method from MythTV.MythDB()
           via 'chanid' and 'starttime'-
        """

        # get the 'progstart' time of the 'recorded' table:
        rec = Recorded((int(self.testenv['RECCHANID']), int(self.testenv['RECSTARTTIMEMYTH'])), db = self.mydb)
        starttime_utc_iso = rec.progstart.utcisoformat() +"Z"
        # use 'progstart' as 'starttime' in the oldrecored table, like '2019-03-05T12:55:00Z':
        recs  =  self.mydb.searchOldRecorded( chanid    = self.testenv['RECCHANID']
                                            , starttime = starttime_utc_iso
                                            )
        rec02 =  next(recs)
        self.assertTrue(isinstance(rec02, OldRecorded))
        # check if accessing a property works
        self.assertTrue(rec02.recordid == int(self.testenv['RECRECORDID']))


class test_Methodheap_MythDB_003(unittest.TestCase):
    """Test method 'searchArtwork' from MythTV.MythDB()."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_003_searchArtwork_01(self):
        """Test 'searchArtwork' method from MythTV.MythDB().
        """

        artwork =  next(self.mydb.searchArtwork())
        self.assertTrue(isinstance(artwork, RecordedArtwork))


    def test_Methodheap_MythDB_003_searchArtwork_02(self):
        """Test 'searchArtwork' method from MythTV.MythDB(),
           given 'chanid', 'starttime'.
        """

        # get the sattime in UTC and ISO format: like '2019-03-05T12:51:00Z'
        starttime_utc_iso = datetime.duck(self.testenv['RECSTARTTIMEMYTH']).utcisoformat() +"Z"
        artworks =  self.mydb.searchArtwork( chanid = self.testenv['RECCHANID']
                                           , starttime = starttime_utc_iso
                                           )
        artwork  =  next(artworks)
        self.assertTrue(isinstance(artwork, RecordedArtwork))
        # check if accessing a property works
        self.assertTrue(artwork.coverart.data == "%s_coverart.jpg" % self.testenv['RECINETREF'])


    def test_Methodheap_MythDB_003_searchArtwork_03(self):
        """Test 'searchArtwork' method from MythTV.MythDB() by given inetref.
        """

        artworks =  self.mydb.searchArtwork( inetref = self.testenv['RECINETREF'])
        artwork  =  next(artworks)
        self.assertTrue(isinstance(artwork, RecordedArtwork))
        # check if accessing a property works
        self.assertTrue(artwork.coverart.data == "%s_coverart.jpg" % self.testenv['RECINETREF'])
        #   or  artwork['coverart']) which results in the same string of jpg file


class test_Methodheap_MythDB_004(unittest.TestCase):
    """Test method 'searchJobs' from MythTV.MythDB()."""

    mydb = MythDB()

    def test_Methodheap_MythDB_004_searchJobs_01(self):
        """Test 'searchJobs' method from MythTV.MythDB().
        """

        jobs =  next(self.mydb.searchJobs())
        self.assertTrue(isinstance(jobs, Job))


class test_Methodheap_MythDB_005(unittest.TestCase):
    """Test method 'searchGuide' from MythTV.MythDB()."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_005_searchGuide_01(self):
        """Test 'searchGuide' method from MythTV.MythDB().
        """

        guide =  next(self.mydb.searchGuide())
        self.assertTrue(isinstance(guide, Guide))

        # test '__repr__' and '__str__'
        print()
        print(repr(guide))
        # print(str(guide))   # XXX this does not work


    def test_Methodheap_MythDB_005_searchGuide_02(self):
        """Test 'searchGuide' method from MythTV.MythDB() using fuzzy title.
        """

        guide_fuzz =  next(self.mydb.searchGuide( fuzzytitle = \
                                            self.testenv['UPTITLEFUZZY']) )
        self.assertTrue(isinstance(guide_fuzz, Guide))
        # check if accessing a property works
        self.assertTrue(self.testenv['UPTITLEFUZZY'] in guide_fuzz.title)


class test_Methodheap_MythDB_006(unittest.TestCase):
    """Test method 'searchRecord' from MythTV.MythDB()."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_006_searchRecord_01(self):
        """Test 'searchRecord' method from MythTV.MythDB()
            using 'title' and 'chanid'.
        """

        programs  =  self.mydb.searchRecord( chanid = self.testenv['UPCHANID']
                                           , title  = self.testenv['UPTITLE'])
        program01 =  next(programs)
        self.assertTrue(isinstance(program01, Record))


    def test_Methodheap_MythDB_006_searchRecord_02(self):
        """Test 'searchRecord' method from MythTV.MythDB()
           using 'title' and 'chanid'.
        """

        programs  =  self.mydb.searchRecord( chanid = self.testenv['UPCHANID']
                                           , title  = self.testenv['UPTITLE'])
        program02 =  next(programs)
        self.assertTrue(isinstance(program02, Record))
        # check if accessing a property works
        self.assertTrue(self.testenv['UPTITLEFUZZY'] in program02.title)


class test_Methodheap_MythDB_007(unittest.TestCase):
    """Test method 'getFrontends' from MythTV.MythDB()."""

    mydb = MythDB()

    def test_Methodheap_MythDB_007_getFrontends_01(self):
        """Test 'getFrontends' method from MythTV.MythDB().

           Note: No frontend will be connected to the test PC!
        """

        try:
            frontends = next(self.mydb.getFrontends())
            print(frontends)
        except StopIteration:
            print("No frontend is connected to the MythTV's python bindings.")
            pass


class test_Methodheap_MythDB_008(unittest.TestCase):
    """Test method 'getFrontend' from MythTV.MythDB()."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_008_getFrontend_01(self):
        """Test 'getFrontend' method from MythTV.MythDB().
        """

        try:
            frontend = self.mydb.getFrontend(self.testenv['FRONTENDNAME'])
        except MythFEError:
            #print('Connection to Frontend failed!')
            pass


class test_Methodheap_MythDB_009(unittest.TestCase):
    """Test method 'scanVideos' from MythTV.MythDB().
    """

    mydb = MythDB()

    def test_Methodheap_MythDB_009_scanVideos_01(self):
        """Test 'scanVideos' method from MythTV.MythDB().
        """

        newvids, movvids, oldvids = self.mydb.scanVideos()
        self.assertTrue(isinstance(newvids, list))
        self.assertTrue(isinstance(movvids, list))
        self.assertTrue(isinstance(oldvids, list))


class test_Methodheap_MythDB_010(unittest.TestCase):
    """Test method 'searchVideos' from MythTV.MythDB().
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def setUp(self):
        self.mydb = MythDB()


    def test_Methodheap_MythDB_010_searchVideos_01(self):
        """Test 'searchVideos' method from MythTV.MythDB()
           using 'title' and 'cast'.
        """

        vids = self.mydb.searchVideos( title = self.testenv['VIDTITLE']
                                     , cast = self.testenv['VIDCAST']
                                     )
        vid = next(vids)
        self.assertTrue(isinstance(vid, Video))


class test_Methodheap_MythDB_100(unittest.TestCase):
    """Test method 'gethostname' from MythTV.MythDB() inherited from DBCache."""

    mydb = MythDB()

    def test_Methodheap_MythDB_100_gethostnames_01(self):
        """Test 'gethostname' method from MythTV.MythDB() inherited from DBCache.
        """

        hname = self.mydb.gethostname()
        #print(hname, type(hname))
        self.assertGreater(len(hname), 0)



class test_Methodheap_MythDB_101(unittest.TestCase):
    """Test method 'getMasterBackend' from MythTV.MythDB() inherited from DBCache."""

    mydb = MythDB()

    def test_Methodheap_MythDB_101_getMasterBackend_01(self):
        """Test 'getMasterBackend' method from MythTV.MythDB() inherited from DBCache.
        """

        master = self.mydb.getMasterBackend()
        #print(master, type(master))
        self.assertGreater(len(master), 0)


class test_Methodheap_MythDB_102(unittest.TestCase):
    """Test method 'getStorageGroup' from MythTV.MythDB() inherited from DBCache."""

    mydb = MythDB()

    def test_Methodheap_MythDB_102_getStorageGroup_01(self):
        """Test 'getStorageGroup' method from MythTV.MythDB() inherited from DBCache.
        """

        sgroups = self.mydb.getStorageGroup(hostname = self.mydb.getMasterBackend())
        sg = next(sgroups)
        sgname = sg[u'groupname']
        #print(sgname, type(sgname))
        self.assertGreater(len(sgname), 0)


if __name__ == '__main__':
    unittest.main()
