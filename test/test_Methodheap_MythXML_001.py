# -*- coding: utf-8 -*-

import unittest
import re
import sys
import socket
import os
from sys      import stdout
from datetime import datetime  as pdtime
from datetime import timedelta as pddelta

from MythTV import Program, MythXML, datetime, System, MythError, MythFileError

from test.helpers import tailandgrep, add_log_flags, get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)

class test_Methodheap_MythXML_001(unittest.TestCase):
    """Test connections class MythXML from MythTV.MythXML."""

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    @classmethod
    def tearDownClass(cls):
        # clear test environment
        global TestEnv
        TestEnv.clear()
        # remove temorary files
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')

    def setUp(self):
        # find recordings for standard times and daylight saving times:
        self.t1_cet  = datetime.frommythtime(int(self.testenv['T1_STDT']))
        self.t2_cet  = datetime.frommythtime(int(self.testenv['T2_STDT']))
        self.t1_cest = datetime.frommythtime(int(self.testenv['T1_ST']))
        self.t2_cest = datetime.frommythtime(int(self.testenv['T2_ST']))

    def test_Methodheap_MythXML_001_01(self):
        """Test MythXML.getHosts()."""
        m_instance  = MythXML()
        hosts = m_instance.getHosts()
        self.assertTrue(socket.gethostname() in hosts)


    def test_Methodheap_MythXML_001_02(self):
        """Test MythXML.getKeys()."""
        m_instance  = MythXML()
        keys_list = m_instance.getKeys()
        self.assertTrue(u'MenuTheme' in keys_list)


    def test_Methodheap_MythXML_001_03(self):
        """Test MythXML.getSetting()."""
        m_instance  = MythXML()
        port = m_instance.getSetting('BackendServerPort', default='1111')
        self.assertTrue(int(port), 6543)


    def test_Methodheap_MythXML_001_04(self):
        """Test MythXML.getProgramGuide()
        """
        now_0 = pdtime.now()
        now_4 = now_0 + pddelta(hours=4)
        m_instance  = MythXML()
        guide_list = m_instance.getProgramGuide( now_0.isoformat()
                                               , now_4.isoformat()
                                               , self.testenv['RECCHANID']
                                               , numchan=None)
        prog = next(guide_list)
        self.assertTrue( len(prog.title) > 0 )


    def test_Methodheap_MythXML_001_05(self):
        """Test MythXML.getProgramDetails().
        """
        now_0 = pdtime.now()
        now_4 = now_0 + pddelta(hours=4)
        m_instance  = MythXML()
        guide_list = m_instance.getProgramGuide( now_0.isoformat()
                                               , now_4.isoformat()
                                               , self.testenv['RECCHANID']
                                               , numchan=None)
        prog = next(guide_list)
        self.assertTrue( len(prog.title) > 0 )
        p_details = m_instance.getProgramDetails(prog.chanid, prog.starttime)
        #print(repr(p_details))
        self.assertTrue( len(p_details.title) > 0 )


    def test_Methodheap_MythXML_001_06(self):
        """Test MythXML.getChannelIcon()
        """
        m_instance  = MythXML()
        icon = m_instance.getChannelIcon(self.testenv['RECCHANID'])
        with open('/tmp/icon', 'wb') as f:
            f.write(icon)
        os.system('file /tmp/icon > /tmp/my_logfile')
        a = ( len(tailandgrep('/tmp/my_logfile', 2, 'JPEG|PNG')) > 0)
        self.assertTrue(a)


    def test_Methodheap_MythXML_001_07(self):
        """Test MythXML.getRecorded()."""
        m_instance  = MythXML()
        rec_list = m_instance.getRecorded()
        rec = next(rec_list)
        self.assertTrue( len(rec.title) > 0 )


    def test_Methodheap_MythXML_001_08(self):
        """Test MythXML.getExpiring()."""
        m_instance  = MythXML()
        rec_list = m_instance.getExpiring()
        rec = next(rec_list)
        self.assertTrue( len(rec.title) > 0 )


    def test_Methodheap_MythXML_001_09(self):
        """Test MythXML.getPreviewImage()."""
        m_instance  = MythXML()
        rec_chanid    = self.testenv['DOWNCHANID']
        rec_starttime = self.testenv['DOWNSTARTTIME']
        preview = m_instance.getPreviewImage( str(rec_chanid),rec_starttime )
        with open('/tmp/preview', 'wb') as f:
            f.write(preview)
        os.system('file /tmp/preview > /tmp/my_logfile')
        a = ( len(tailandgrep('/tmp/my_logfile', 2, 'JPEG|PNG')) > 0)
        self.assertTrue(a)


    def test_Methodheap_MythXML_001_010(self):
        """Test MythXML.getRecorded() during standard time and
           daylight saving time.
        """
        preview_cet_is_pic  = False
        preview_cest_is_pic = False

        m_instance  = MythXML()
        progs = m_instance.getRecorded()
        try:
            found_cet  = False
            found_cest = False
            while True:
                p = next(progs)
                if not found_cet:
                    if ( p.starttime > self.t1_cet and p.starttime < self.t2_cet):
                        pcet = p
                        found_cet = True
                if not found_cest:
                    if ( p.starttime > self.t1_cest and p.starttime < self.t2_cest):
                        pcest = p
                        found_cest = True
                if (found_cet and found_cest):
                    break
        except StopIteration:
            raise

        preview_cet = m_instance.getPreviewImage( str(pcet.chanid), pcet.recstartts )
        with open('/tmp/preview_cet', 'wb') as f:
            f.write(preview_cet)
        s_cet = System(path='file')
        out_cet = s_cet('/tmp/preview_cet')
        preview_cet_is_pic = ( (b'PNG' in out_cet) or (b'JPEG' in out_cet) )

        preview_cest = m_instance.getPreviewImage( str(pcest.chanid), pcest.recstartts )
        with open('/tmp/preview_cest', 'wb') as f:
            f.write(preview_cest)
        s_cest = System(path='file')
        out_cest = s_cest('/tmp/preview_cest')
        preview_cest_is_pic = ( (b'PNG' in out_cest) or (b'JPEG' in out_cest) )

        self.assertTrue(preview_cet_is_pic)
        self.assertTrue(preview_cest_is_pic)


    def tearDown(self):
        if os.path.exists('/tmp/icon'):
            os.remove('/tmp/icon')
        if os.path.exists('/tmp/my_logfile'):
            os.remove('/tmp/my_logfile')
        if os.path.exists('/tmp/preview'):
            os.remove('/tmp/preview')
        if os.path.exists('/tmp/preview_cet'):
            os.remove('/tmp/preview_cet')
        if os.path.exists('/tmp/preview_cest'):
            os.remove('/tmp/preview_cest')


if __name__ == '__main__':
    unittest.main()
