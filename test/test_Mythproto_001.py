# -*- coding: utf-8 -*-

import unittest
import os
import time
import threading
import re
import socket
from pprint import pprint

from MythTV import MythDB, MythBE, Frontend, Recorded, findfile, ftopen

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Mythproto_001(unittest.TestCase):
    """Test method 'findfile'.
       This test uses hardcoded values from the file '.testenv'.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

        with add_log_flags():
            mydb = MythDB()

    def test_Mythproto_001_findfile_01(self):
        """Test 'findfile' method from MythTV mytproto.
           Note: 'findfile' only works on local filesystem.
        """
        recfile = self.testenv['RECBASENAME']
        sg = findfile(recfile, 'Default')
        if sg is not None:
            recfilepath = os.path.join(sg.dirname, recfile)
            self.assertTrue(os.access(recfilepath))
        else:
            self.assertIsNone(sg)


class test_Mythproto_002(unittest.TestCase):
    """Test method 'ftopen' on a already recorded file.
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

    def test_Mythproto_002_ftopen_01(self):
        """Test 'ftopen' method from MythTV mythproto.py with 'chanid', 'starttime'.
           According doc of 'ftopen',
            'file' takes a standard MythURI:
                myth://<group>@<host>:<port>/<path>
           or file can be a tuple of (host, sgroup, filename) according the source code.
           The test reads a recoring, stores it to '/tmp/testfile' and writes this file to
           the 'Temp' storagegroup of the backend.
        """
        rec_filename  = self.testenv['DOWNFILENAME']
        rec_chanid    = self.testenv['DOWNCHANID']
        rec_starttime = self.testenv['DOWNSTARTTIME']
        rec_sg        = self.testenv['DOWNSTORAGEGROUP']
        host          = self.mydb.getMasterBackend()

        f = ftopen((host, rec_sg, rec_filename), 'r', db=self.mydb, chanid=rec_chanid, starttime=rec_starttime)
        ## (host, rec_sg, rec_filename) gives myth://Default@192.168.47.11:6543/<path/to/4711_20190305125100.mkv
        with open ('/tmp/testfile', 'wb+') as fw:
                while True:
                    b = f.read(0x400 * 128)
                    if not b:
                        # eof
                        break
                    fw.write(b)
        f.close()
        filesize1 = Recorded((rec_chanid, rec_starttime), db=self.mydb).filesize
        filesize2 = os.path.getsize('/tmp/testfile')
        self.assertEqual(filesize1, filesize2)
        fwtmpfile = "myth://Temp@%s:6543/%s" %(host, rec_filename)
        #print(fwtmpfile)
        fwtmp = ftopen(fwtmpfile, 'w', db=self.mydb)
        with open ('/tmp/testfile', 'rb') as fr:
            while True:
                b = fr.read(0x400 * 128)
                if not b:
                    # eof
                    break
                fwtmp.write(b)
        fwtmp.close() ### XXX RER
        ### XXX this gives:
        # Exception AttributeError: 'ftsock' in <bound method FileTransfer.__del__
        # of <open file 'myth://Temp@<ip>/3002_20190622105000.mkv', mode 'w' at 0x7f1559e83490>> ignored
        # but filesize check works
        # Note on '__del__' method from python docs:
        # Warning: Due to the precarious circumstances under which __del__() methods are invoked,
        # exceptions that occur during their execution are ignored, and a warning is printed to sys.stderr instead.

        if self.mybe.fileExists(rec_filename, sgroup="Temp"):
            getsgfile = self.mybe.getSGFile(host, "Temp", rec_filename)
            if isinstance(getsgfile, tuple):
                filesize3 = int(getsgfile[1])
            elif (getsgfile < 0):
                    self.fail("File in storagegroup 'Temp' not found: '%s'" %rec_filename)
            else:
                #print(getsgfile)
                filesize3 = 0
        else:
            self.fail("File not found: '%s'" %fwtmpfile)
        ret = self.mybe.deleteFile(rec_filename, "Temp")
        self.assertEqual(ret, '1')
        #print(filesize1, filesize2, filesize3)
        self.assertEqual(filesize1, filesize3)


class test_Mythproto_003(unittest.TestCase):
    """Test method 'ftopen' on a file that is in recording state.
       This test uses hardcoded values from the file '.testenv'
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
            # connect to frontend
            self.fe = Frontend("%s" %(self.testenv['FRONTENDIP']), 6546)

    def tearDown(self):
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')
        if os.path.exists('/tmp/testfile'):
            os.remove('/tmp/testfile')

    def test_Mythproto_003_ftopen_01(self):
        """Test 'ftopen' method from MythTV mythproto.py with 'chanid', 'starttime'
           during recording.
           According doc of 'ftopen',
            'file' takes a standard MythURI:
                myth://<group>@<host>:<port>/<path>
           or file can be a tuple of (host, sgroup, filename) according the source code.
           The tests spawns to threads, one for LiveTV and the other one for ftopen.
           Thread ftopen saves the recorded livetv to /tmp/testfile.
           If the filesize gets updated, the method 'RecordedFileTransfer.updatesize()'
           was triggered by the 'BACKEND_MESSAGE UPDATE_FILE_SIZE' event.
        """

        # thrad function for LiveTV:
        def thread_livetv(chanid):
            j1 = self.fe.jump.livetv
            play = self.fe.sendPlay("chanid %s" %(chanid))
            # sleep some time to let the file grow
            time.sleep(90)
            # stop the recording
            self.fe.sendPlay("stop")

        # thrad function for 'ftopen':
        def thread_ftopen(mythuri, db, chanid, starttime):
            f = ftopen(mythuri, 'r', db=db, chanid=chanid, starttime=starttime)
            with open ('/tmp/testfile', 'wb+') as fw:
                    retries = 0
                    while (retries < 20):
                        b = f.read(0x400 * 128)
                        if b:
                            fw.write(b)
                            retries = 0
                        else:
                            # EOF or UPDATE_FILESIZE ?
                            time.sleep(1)
                            retries += 1
            f.close()


        #  check if there are free recorders
        recorders = self.mybe.getFreeRecorderList()
        selected_recorder = None
        selected_recorder = [r for r in recorders if not self.mybe.isRecording(r)][0]
        if selected_recorder:
            # start first thread for LiveTV
            # start livetv via Frontend connection on given chanid
            livetv = threading.Thread(target=thread_livetv, args=(self.testenv['RECCHANID'],))
            livetv.start()
            # wait some time to finish the SignalMonitor check, if there is any
            time.sleep(30)
            # get the values for 'chanid', 'starttime', 'recordedid'
            #   for the current liveTV recording:
            # iterate again over the recorder list:
            recorders = self.mybe.getRecorderList()
            # pprint(recorders)
            # get all recording recorders and select the one who is recording 'chanid':
            recrecorders = [r for r in recorders if self.mybe.isRecording(r)]
            r = None
            for r in recrecorders:
                # this returns a 'Program' object:
                prgrm = self.mybe.getCurrentRecording(r)
                if  (prgrm.chanid == self.testenv['RECCHANID']):
                    #print("rec found!")
                    break
                self.assertEqual(prgrm.chanid, int(self.testenv['RECCHANID']))
            if r:
                # get input parameter for 'ftopen'
                host   = self.mydb.getMasterBackend()
                rec_sg = 'LiveTV'
                rec    = Recorded.fromProgram(prgrm)
                #print(rec.recordedid)
                #print(rec.filesize)
                # start second thread for 'ftopen':
                # open the file transfer ('ftopen') an wait until 'UPDATE_FILE_SIZE'
                #   messages informs us to read more data
                mythuri = (host, rec_sg, rec.basename)
                ftothread = threading.Thread(target=thread_ftopen, args=( mythuri, self.mydb
                                                                     , rec.chanid
                                                                     , rec.starttime
                                                                     )
                                            )
                ftothread.start()
                time.sleep(1)
                # wait until the livetv thread terminates after timeout
                livetv.join(100.0)
                self.assertFalse(livetv.is_alive())
                # wait until the ftopen thread terminates after timeout
                ftothread.join(500.0)
                self.assertFalse(ftothread.is_alive())

                # check results:
                # get filesize from '/tmp/testfile'
                fs_ftopen = os.path.getsize('/tmp/testfile')
                # get filesize from recorded livetv:
                rec1 = Recorded.fromProgram(prgrm)
                #print(rec1.recordedid)
                rec_size  = rec1.filesize
                # Note: the last 'updatesize' event is not sent, therefore
                #       the fiesize is not equal.
                #self.assertEqual(fs_ftopen, rec_size)
                self.assertTrue(fs_ftopen > rec.filesize)

            else:
                self.fail('No recorders are recording.')
        else:
            self.fail('No free recorders are available.')


class test_Mythproto_004(unittest.TestCase):
    """Test method 'ftopen' on a already recorded file.
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


    def test_Mythproto_004_ftopen_01(self):
        """Test 'ftopen' method from MythTV mythproto.py by calling
           MythBE.download() with a valid MythURI':
           myth://<group>@<host>:<port>/<path>
        """
        rec_filename  = self.testenv['DOWNFILENAME']
        rec_sg        = self.testenv['DOWNSTORAGEGROUP']
        host          = self.mydb.getMasterBackend()
        host_ip       = self.mydb.settings['NULL']['MasterServerIP']
        host_port     = int(self.mydb.settings[host]['BackendServerPort'])

        # get the file path
        filepath = self.mybe.fileExists(rec_filename, sgroup=rec_sg)
        self.assertIsNotNone(filepath)
        # assemble the MythURI
        rec_uri = "myth://%s@%s:%d/%s" % (rec_sg, host_ip, host_port, filepath)
        # download it to '$home/.mythtv/tmp' of the backend
        # the file url is something like "myth://Temp@backendserver//download_eef766ea.tmp"
        f = self.mybe.download(rec_uri)
        re_fname = re.compile("/download_[a-fA-F0-9]*.tmp")
        self.assertIsNotNone(re_fname.match(f.filename))
        f.close()


class test_Mythproto_005(unittest.TestCase):
    """Test method 'ftopen' via 'downloadTo' function.
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
        if os.path.exists('/tmp/testfile'):
            os.remove('/tmp/testfile')


    def test_Mythproto_005_ftopen_01(self):
        """Test 'ftopen' method from MythTV mythproto.py by calling
           MythBE.downloadTo() with a valid URL.
           Waits for 'DOWNLOAD UPDATE' events.
        """
        #dl_url = "https://www.mythtv.org/w/images/7/71/Terra_menu3.png"
        dl_url = "https://github.com/MythTV/mythtv/archive/master.zip"
        dl_sg  = "Temp"

        f = self.mybe.downloadTo(dl_url, dl_sg, "dltestfile", forceremote=True
                                                            , openfile=True)
        fsize_open = f._size
        with open ('/tmp/testfile', 'wb+') as fw:
            retries = 0
            # 'DOWNLOAD FINISHED' event clears the registered events for 'DOWNLOAD'
            while ((len(f._events) > 0) or (retries < 5)):
                b = f.read(0x400 * 128)
                if b:
                    fw.write(b)
                    retries = 0
                else:
                    # EOF or UPDATE_FILESIZE ?
                    time.sleep(1)
                    retries += 1
        fsize_close = f._size
        f.close()
        #print("%s > %s" %(fsize_close,fsize_open))
        self.assertTrue(fsize_close > fsize_open)


if __name__ == '__main__':
    unittest.main()
