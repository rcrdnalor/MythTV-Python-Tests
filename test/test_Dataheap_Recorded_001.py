# -*- coding: utf-8 -*-

import unittest
import os
import time
import re

from pprint import pprint

from MythTV import MythDB, MythBE, Frontend, Recorded, Artwork, RecordedArtwork, Program, VideoMetadata, ftopen, datetime
from MythTV.static  import RECSTATUS

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Recorded_001(unittest.TestCase):
    """Test class 'Recorded' from 'dataheap'.
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
            self.mybe = MythBE(db=self.mydb)

    def tearDown(self):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

    def test_Dataheap_Recorded_001_01(self):
        """Test property 'artwork' in class 'Recorded' from 'dataheap'.
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        artwork = rec.artwork
        self.assertTrue(isinstance(artwork, RecordedArtwork))
        self.assertTrue(isinstance(artwork.coverart, Artwork))

    def test_Dataheap_Recorded_001_02(self):
        """Test method 'getProgram()' in class 'Recorded' from 'dataheap'.
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        prgrm = rec.getProgram()
        self.assertTrue(isinstance(prgrm, Program))
        self.assertEqual(RECSTATUS.rsRecorded, prgrm.rsRecorded)


    def test_Dataheap_Recorded_001_03(self):
        """Test method 'getRecordedProgram()' in class 'Recorded' from 'dataheap'.
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        prgrm = rec.getRecordedProgram()
        self.assertEqual(prgrm.chanid, int(chanid))


    def test_Dataheap_Recorded_001_04(self):
        """Test method 'formatPath()' in class 'Recorded' from 'dataheap'.
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        formatpath = rec.formatPath("%U/%T/%pY-%pm-%pd %pH.%pi %T")
        ###print(rec.formatPath("%U/%T/%pY-%pm-%pd %pH.%pi %T"))
        self.assertTrue(title in formatpath)


    def test_Dataheap_Recorded_001_05(self):
        """Test method 'exportMetadata()' in class 'Recorded' from 'dataheap'.
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        metadata = rec.exportMetadata()
        self.assertTrue(isinstance(metadata, VideoMetadata))
        self.assertEqual(metadata.inetref, inetref)


    def test_Dataheap_Recorded_001_06(self):
        """Test method 'Recorded.importMetadata()' and 'Recorded.update()'
           in class 'Recorded' from 'dataheap'.
           Test Case:
           - get a recording
           - save the 'stars' value of the recording for later use
           - save the dictdata of the recording for later use
           - export the metadata to xml and save for later use
           - check xml metatdata structure for the 'stars' i.e. 'userrating' value
           - change the 'stars' value and save it for later use
           - update (save to database) the recording with the new 'stars' value
           - get the recording again to a new instance
           - check the updated 'stars' value
           - import the saved metadata back to the reocrding
           - check the reverted 'stars' value
           - check that the dictionary from the new Recorded instance is compatible to the original one:
           - update Recorded.stars to the original value
           - check for correct value of stars in final instance of Recoreded
        """
        chanid        = self.testenv['RECCHANID']
        starttimeutc  = self.testenv['RECSTARTTIMEUTC']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']
        basename      = self.testenv['RECBASENAME']
        recordedid    = self.testenv['RECRECORDID']
        inetref       = self.testenv['RECINETREF']
        stars         = self.testenv['RECSTARS']

        # Update database in case of any errors from previous test runs
        reczero= Recorded((chanid, starttimemyth), db = self.mydb)
        reczero.stars = stars
        reczero.update()

        rec = Recorded((chanid, starttimemyth), db = self.mydb)
        # save the 'stars' value i.e. 'userrating'
        recstars = rec.stars
        self.assertEqual("%.1f" %recstars, stars)
        # Recorded._origdata holds the dictionary pulled from database
        recdict = {}
        for key, value in rec._origdata.items():
            if isinstance(value, datetime):
                recdict[key] = value.mythformat()
            else:
                recdict[key] = value
        # export the metadata to xml and save for later use
        recmd = rec.exportMetadata()
        recmdxml = recmd.toXML()
        # check xml metadata structure for the 'stars' i.e. 'userrating' value
        # see https://www.mythtv.org/wiki/MythTV_Universal_Metadata_Format
        tree = recmdxml.getroottree()
        ### pprint(tree)    # lxml stuff
        recmdxml_stars = next(tree.iter('userrating')).text
        self.assertEqual("%.1f" %float(recmdxml_stars), stars)
        # change the 'stars' value and save it for later use
        rec.stars += 0.1
        recstars_updated = rec.stars
        # update (save to database) the recording with the new 'stars' value
        rec.update()
        # get the recording again to a new instance
        recnew = Recorded((chanid, starttimemyth), db = self.mydb)
        # check the updated 'stars' value
        self.assertEqual(recnew.stars, recstars_updated)
        # import the saved metadata back to the reocrding
        # Note: Recorded.importMetadata() make an implicit Recorded.update()
        recnew.importMetadata(recmd, overwrite=True)
        # check the reverted 'stars' value
        self.assertEqual("%.1f" %recnew.stars, stars)
        # check that the dictionary from the new Recorded instance is compatible to the original one:
        for key, value in recdict.items():
            if isinstance(recnew._origdata[key], datetime):
                # don't act on 'lastmodified' entry, because we changed the rec in between:
                if key != 'lastmodified':
                    self.assertEqual(recdict[key], recnew._origdata[key].mythformat())

        self.assertEqual(len(recdict), len(recnew._origdata))
        # update Recorded.stars to the original value
        recnew.stars = recstars
        recnew.update()
        # check for correct value of stars in final instance of Recoreded
        reclast = Recorded((chanid, starttimemyth), db = self.mydb)
        self.assertEqual("%.1f" %reclast.stars, stars)

if __name__ == '__main__':
    unittest.main()
