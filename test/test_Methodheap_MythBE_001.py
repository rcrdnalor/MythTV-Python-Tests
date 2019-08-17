# -*- coding: utf-8 -*-

import unittest
import time
import os
import subprocess
import re

from datetime import timedelta

from MythTV import MythDB, MythBE, Program, MythLog, FreeSpace

from test.helpers import tailandgrep, add_log_flags, get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Methodheap_MythBE_001(unittest.TestCase):
    """Test method 'getPendingRecordings' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_001_getPendingRecordings_01(self):
        """Test 'getPendingRecordings' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recs01 = BE.getPendingRecordings()
        rec01 = next(recs01)
        self.assertTrue(isinstance(rec01, Program))


class test_Methodheap_MythBE_002(unittest.TestCase):
    """Test method 'getScheduledRecordings' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_002_getScheduledRecordings_01(self):
        """Test 'getScheduledRecordings' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        rec02 = next(BE.getScheduledRecordings())
        self.assertTrue(isinstance(rec02, Program))


class test_Methodheap_MythBE_003(unittest.TestCase):
    """Test method 'getUpcomingRecordings' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_003_getUpcomingRecordings_01(self):
        """Test 'getUpcomingRecordings' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        rec03 = next(BE.getUpcomingRecordings())
        self.assertTrue(isinstance(rec03, Program))


class test_Methodheap_MythBE_004(unittest.TestCase):
    """Test method 'getConflictedRecordings' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_004_getConflictedRecordings_01(self):
        """Test 'getConflictedRecordings' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        try:
            rec04 = next(BE.getConflictedRecordings())
            self.assertTrue(isinstance(rec04, Program))
        except StopIteration:
            pass

class test_Methodheap_MythBE_005(unittest.TestCase):
    """Test method 'getRecorderList' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_005_getRecorderList_01(self):
        """Test 'getRecorderList' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recorders = BE.getRecorderList()
        self.assertTrue(isinstance(recorders, list))


class test_Methodheap_MythBE_006(unittest.TestCase):
    """Test method 'getFreeRecorderList' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_006_getFreeRecorderList_01(self):
        """Test 'getFreeRecorderList' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        freerecorders = BE.getFreeRecorderList()
        self.assertTrue(isinstance(freerecorders, list))


class test_Methodheap_MythBE_007(unittest.TestCase):
    """Test method 'getFreeInputInfo' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_007_getFreeInputInfo_01(self):
        """Test 'getFreeInputInfo' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        freeinfo = BE.getFreeInputInfo()
        self.assertTrue(isinstance(freeinfo, list))
        self.assertTrue(isinstance(freeinfo[0], BE._InputInfo))


# class test_Methodheap_MythBE_008(unittest.TestCase):
#     """Test method 'lockTuner', 'freeTuner' from MythTV.MythBE()."""

#     def test_Methodheap_MythBE_008_lock_freeTuner_01(self):
#         """Test  'lockTuner', 'freeTuner' methods from MythTV.MythBE().
#         """
#         DB = MythDB()
#         BE = MythBE(db=DB)
#         free_recorders = BE.getFreeRecorderList()
#         #print(free_recorders)
#         #res_lock = BE.lockTuner(14)
#         res_lock = BE.lockTuner()
#         if isinstance(res_lock, tuple):
#             # good case
#             #print(res_lock)
#             time.sleep(5)
#             l_free_recorders = BE.getFreeRecorderList()
#             #print(l_free_recorders)
#         else:
#             # unsuccessfull
#             l_free_recorders = free_recorders
#         #res_unlock = BE.freeTuner(14)
#         res_unlock = BE.freeTuner()
#         #print(res_unlock)
#         time.sleep(5)
#         u_free_recorders = BE.getFreeRecorderList()
#         #print(u_free_recorders)
#         self.assertTrue(u_free_recorders == free_recorders)


class test_Methodheap_MythBE_009(unittest.TestCase):
    """Test method 'getCurrentRecording' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_009_getCurrentRecording_01(self):
        """Test 'getCurrentRecording' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recorders = BE.getRecorderList()
        curr_rec = None
        for r in recorders:
            if BE.isRecording(r):
                curr_rec = BE.getCurrentRecording(r)
                #print(curr_rec.title)
        self.assertTrue( (isinstance(curr_rec, Program)) | (curr_rec is None) )


class test_Methodheap_MythBE_010(unittest.TestCase):
    """Test method 'isRecording' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_010_isRecording_01(self):
        """Test 'isRecording' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recorder0 = BE.getFreeRecorderList()[0]
        isRecording =  BE.isRecording(recorder0)
        self.assertIsNotNone(isRecording)     # either True or False


class test_Methodheap_MythBE_011(unittest.TestCase):
    """Test method 'isActiveBackend' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_011_isActiveBackend_01(self):
        """Test 'isActiveBackend' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        master = DB.getMasterBackend()
        active = BE.isActiveBackend(master)
        self.assertTrue(active)


class test_Methodheap_MythBE_012(unittest.TestCase):
    """Test method 'getRecordings' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_012_getRecordings_01(self):
        """Test 'getRecordings' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recs = BE.getRecordings()
        self.assertTrue(isinstance(next(recs), Program))


class test_Methodheap_MythBE_013(unittest.TestCase):
    """Test method 'getExpiring' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_013_getExpiring_01(self):
        """Test 'getExpiring' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        recs = BE.getExpiring()
        self.assertTrue(isinstance(next(recs), Program))


class test_Methodheap_MythBE_014(unittest.TestCase):
    """Test method 'getCheckfile' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_014_getExpiring_01(self):
        """Test 'getCheckfile' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        rec = next(BE.getExpiring())
        loc = BE.getCheckfile(rec)
        self.assertTrue('/' in loc)


class test_methodheap_mythbe_015(unittest.TestCase):
    """test method 'getFreeSpace' from mythtv.mythbe()."""

    def test_methodheap_mythbe_015_getFreeSpace_01(self):
        """test 'getFreeSpace' method from mythtv.mythbe().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        free_space_01 = next(BE.getFreeSpace(all=False))
        self.assertTrue(isinstance(free_space_01, FreeSpace))

    def test_methodheap_mythbe_015_getFreeSpace_02(self):
        """test 'getFreeSpace' method from mythtv.mythbe().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        free_space_02 = next(BE.getFreeSpace(all=True))
        self.assertTrue(isinstance(free_space_02, FreeSpace))


class test_Methodheap_MythBE_016(unittest.TestCase):
    """Test method 'getFreeSpaceSummary' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_016_getFreeSpaceSummary_01(self):
        """Test 'getFreeSpaceSummary' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        free_space_sum = BE.getFreeSpaceSummary()
        self.assertTrue(isinstance(free_space_sum, tuple))
        #print(free_space_sum)


class test_Methodheap_MythBE_017(unittest.TestCase):
    """Test method 'getLoad' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_017_getLoad_01(self):
        """Test 'getLoad' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        load = BE.getLoad()
        self.assertTrue(isinstance(load, list))
        self.assertTrue(isinstance(load[0], float))


class test_Methodheap_MythBE_018(unittest.TestCase):
    """Test method 'getUptime' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_018_getUptime_01(self):
        """Test 'getUptime' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        td = BE.getUptime()
        self.assertTrue(isinstance(td, timedelta))


class test_Methodheap_MythBE_019(unittest.TestCase):
    """Test method 'walkSG' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_019_walkSG_01(self):
        """Test 'walkSG' method from MythTV.MythBE().
           'walkSG' returns  [('/', (), {'1234_20180718181100.mkv.-1.100x75.png': '12482'
                                       , '4578_20190531104800.ts': '2956729956',....})]
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        host = BE.hostname
        storagegroup = 'Default'
        t = BE.walkSG(host, storagegroup)
        self.assertTrue(isinstance(t, list))
        for el in t:
            self.assertTrue(isinstance(el, tuple))
            self.assertTrue(isinstance(el[0], str))
            self.assertTrue(isinstance(el[1], tuple))
            self.assertTrue(isinstance(el[2], dict))


class test_Methodheap_MythBE_020(unittest.TestCase):
    """Test method 'getSGList' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_020_getSGList_01(self):
        """Test 'getSGList' method from MythTV.MythBE().
           'getSGList' returns a list of dirnames if path is empty.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        host = BE.hostname
        storagegroup = 'Default'
        t = BE.getSGList(host, storagegroup, '')
        self.assertTrue(isinstance(t, list))

    def test_Methodheap_MythBE_020_getSGList_02(self):
        """Test 'getSGList' method from MythTV.MythBE().
           'getSGList'returns a list of filenames, when filenamesonly=True.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        host = BE.hostname
        storagegroup = u'Default'
        t = BE.getSGList(host, storagegroup, '', filenamesonly=True)
        self.assertTrue(isinstance(t, list))


class test_Methodheap_MythBE_021(unittest.TestCase):
    """Test method 'getSGFile' from MythTV.MythBE()."""

    def test_Methodheap_MythBE_021_getSGFile_01(self):
        """Test 'getSGFile' method from MythTV.MythBE().
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        host = BE.hostname
        storagegroup = 'Default'
        # get the path:
        p = BE.getSGList(host, storagegroup ,'', filenamesonly=True)
        path = p[0]
        # get the filename:
        f = BE.getSGList(host, storagegroup ,'')
        filename = f[0]
        filepath = os.path.join(path, filename)
        sgfile = BE.getSGFile(host, storagegroup, path)
        if len(sgfile) > 1:
            # file found and filesize can be determined:
            self.assertTrue(isinstance(int(sgfile[1]), int))
        else:
            self.assertLess(len(sgfile), 2)


class test_Methodheap_MythBE_101(unittest.TestCase):
    """Test method 'getRecording' from MythTV.MythBE() inherited from FileOps.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv


    def test_Methodheap_MythBE_101_getRecording_01(self):
        """Test 'getRecording' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        chanid = self.testenv['RECCHANID']
        starttime = int(self.testenv['RECSTARTTIMEMYTH'])
        prgrm = BE.getRecording(chanid, starttime)
        #print(prgrm.toString())
        self.assertTrue(isinstance(prgrm, Program))


class test_Methodheap_MythBE_102(unittest.TestCase):
    """Test method 'forgetRecording' from MythTV.MythBE() inherited from FileOps.
       According wiki, this marks 'old recordings' as never duplicates,
       so they can be re-recorded.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv


    def test_Methodheap_MythBE_102_forgetRecording_01(self):
        """Test 'forgetRecording' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        chanid = self.testenv['RECCHANID']
        starttime = int(self.testenv['RECSTARTTIMEMYTH'])
        prgrm = BE.getRecording(chanid, starttime)
        #print(prgrm.toString())
        self.assertTrue(isinstance(prgrm, Program))
        try:
            # This forces a reschedule on the backend for the given program:
            BE.forgetRecording(prgrm)
        except:
            self.fail()


class test_Methodheap_MythBE_103(unittest.TestCase):
    """Test method 'deleteRecording' from MythTV.MythBE() inherited from FileOps.
    """

    def test_Methodheap_MythBE_103_deleteRecording_01(self):
        """Test 'deleteRecording' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        # get the expiring list
        prgrm = next(BE.getExpiring())
        self.assertTrue(isinstance(prgrm, Program))
        ### XXX it works, but I won't do this often
#        retval = BE.deleteRecording(prgrm)
#        # Even wiki says, retval '-1' is correct, this returns '0' on success, because
#        # the backend log states: " Reschedule requested for CHECK 0 10965 737562 DoHandleDelete1"
#        self.assertEqual(retval, '0')


class test_Methodheap_MythBE_104(unittest.TestCase):
    """Test method 'deleteFile' from MythTV.MythBE() inherited from FileOps.
    """

    def test_Methodheap_MythBE_104_deleteFile_01(self):
        """Test 'deleteFile' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        master_backend_ip = DB.settings['NULL']['MasterServerIP']
        # get the storagegroup
        sgs = list(DB.getStorageGroup(groupname='Default'))
        # get the path
        path = sgs[0].dirname
        # create an arbitrary file
        pfile = os.path.join(path, 'ptest.txt')
        cmd = "ssh mythtv@%s 'touch %s'" %(master_backend_ip, pfile)
        result = subprocess.call(cmd, shell=True)
        self.assertTrue(result == 0)
        # delete the file
        # full path with file does not work, see backend log:
        # retval = BE.deleteFile(pfile, 'Default')
        retval = BE.deleteFile('ptest.txt', 'Default')
        self.assertEqual(retval, '1')


class test_Methodheap_MythBE_105(unittest.TestCase):
    """Test method 'getHash' from MythTV.MythBE() inherited from FileOps.
    """

    def test_Methodheap_MythBE_105_getHash_01(self):
        """Test 'getHash' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        #get a file from default storagegroup
        host = BE.hostname
        storagegroup = 'Default'
        f = BE.getSGList(host, storagegroup ,'', filenamesonly=True)
        # check if it is a recording
        for rec in f:
          if (rec.rsplit(".", 1)[1] == "ts"):
            break
        retval = BE.getHash(rec, 'Default')
        # check if retval is hexadecimal:
        hex_set = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}
        self.assertTrue(set(retval.lower()).issubset(hex_set))


class test_Methodheap_MythBE_106(unittest.TestCase):
    """Test method 'reschedule' from MythTV.MythBE() inherited from FileOps.
    """
    DB = MythDB()
    BE = MythBE(db=DB)

    def test_Methodheap_MythBE_106_reschedule_01(self):
        """Test 'reschedule' method from MythTV.MythBE() inherited from FileOps.
        """
        self.BE.reschedule(recordid=-1, wait=True)

    def test_Methodheap_MythBE_106_reschedule_02(self):
        """Test 'reschedule' method from MythTV.MythBE() inherited from FileOps.
        """
        self.BE.reschedule(recordid=0)


class test_Methodheap_MythBE_107(unittest.TestCase):
    """Test method 'fileExists' from MythTV.MythBE() inherited from FileOps.
    """

    def test_Methodheap_MythBE_107_fileExists_01(self):
        """Test 'fileExists' method from MythTV.MythBE() inherited from FileOps.
        """
        DB = MythDB()
        BE = MythBE(db=DB)
        #get a file from default storagegroup
        host = BE.hostname
        storagegroup = 'Default'
        f = BE.getSGList(host, storagegroup ,'', filenamesonly=True)
        # check if it is a recording
        for rec in f:
          if (rec.rsplit(".", 1)[1] == "ts"):
            break
        retval = BE.fileExists(rec, 'Default')
        self.assertIsNotNone(retval)



if __name__ == '__main__':
    unittest.main()
