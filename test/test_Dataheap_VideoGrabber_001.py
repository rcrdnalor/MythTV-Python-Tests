# -*- coding: utf-8 -*-

import unittest
import os
from pprint import pprint
from lxml import etree

#from MythTV import MythDB, RecordedArtwork, Video, VideoGrabber

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}


def rewrite_static_prefix(rewrt_file, org_file, new_prefix):
    """Rewrites the 'INSTALL_PREFIX' in static.py to 'new_prefix'"""
    if os.path.isfile(rewrt_file):
        # copy the file to 'static.org'
        if not os.path.isfile(org_file):
            os.system("cp -a %s %s" %(rewrt_file, org_file))
            #print("file copied %s" %rewrt_file)
        # read in and replace existing line
        buff = []
        with open(rewrt_file, 'r') as fi:
            for line in fi:
                if 'INSTALL_PREFIX' in line:
                    line = "INSTALL_PREFIX = '%s'\n" % new_prefix
                buff.append(line)
        # push back to file
        with open(rewrt_file,'w') as fo:
            fo.write(''.join(buff))
        return(True)
    else:
        return(False)

def restore_static_prefix(rewrt_file, org_file):
    if os.path.isfile(org_file):
        if os.path.isfile(rewrt_file):
            os.remove(rewrt_file)
        os.rename(org_file, rewrt_file)
        return(True)
    else:
        return(False)


def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)
    # Fake the INSTALL_PREFIX for metadata lookup, this gives
    # './share/mythtv/metadata/Television/ttvdb.py'
    # './share/mythtv/metadata/Movie/tmdb3.py'
    # $ mkdir -p ./share/mythtv/metadata/Television
    # $ mkdir -p ./share/mythtv/metadata/Movie
    # and copy the scripts from
    # mythtv/programs/scripts/metadata/Movie/tmdb3.py
    # mythtv/programs/scripts/metadata/Television/ttvdb.py
    # set the PYTHONPATH
    # export PYTHONPATH=`pwd`

    cwd = os.getcwd()
    rewrt_file = os.path.join(cwd, "MythTV", "static.py")
    org_file   = os.path.join(cwd, "MythTV", "static.org")

    rewrite_static_prefix(rewrt_file, org_file, cwd)

    from MythTV.static import INSTALL_PREFIX

    global INSTALL_PREFIX
    #print(INSTALL_PREFIX)


def tearDownModule():
    cwd = os.getcwd()
    rewrt_file = os.path.join(cwd, "MythTV", "static.py")
    org_file   = os.path.join(cwd, "MythTV", "static.org")
    restore_static_prefix(rewrt_file, org_file)


class test_Dataheap_VideoGrabber_001(unittest.TestCase):
    """Test class 'VideoGrabber' from dataheap.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv
        global INSTALL_PREFIX
        cls.INSTALL_PREFIX = INSTALL_PREFIX


    def setUp(self):
        if (self.INSTALL_PREFIX != os.getcwd()):
            self.fail("Unable to rewrite 'INSTALL_PREFIX' in static.py!")

    def tearDown(self):
        if os.path.exists("/tmp/my_logfile"):
            os.remove("/tmp/my_logfile")
        if os.path.exists("/tmp/details.xml"):
            os.remove("/tmp/details.xml")


    def test_Dataheap_VideoGrabber_001_sortedSearch_01(self):
        """Test 'sortedSearch' method from MythTV.VideoGrabber
           using predefined  values.
        """
        from MythTV import MythDB, RecordedArtwork, Video, VideoGrabber

        with add_log_flags():
            self.mydb =  MythDB()

            title      = self.testenv['VIDTITLE_DE']
            cast       = self.testenv['VIDCAST_DE']
            inetrefstr = self.testenv['VIDINETREF_DE']
            lang       = self.testenv['VIDLANGUAGE_DE']

            # remove grabber from inetref:
            try:
                inetref = inetrefstr.split('_')[-1]
            except IndexError:
                inetref = inetrefstr

            grab = VideoGrabber("Movie", lang=lang, db=self.mydb)
            metadatalist = grab.sortedSearch(title, subtitle=None, tolerance=2)
            inetref_found = False
            for m in metadatalist:
                if (m.inetref == inetref):
                    inetref_found = True
                    break
            self.assertTrue(inetref_found)


    def test_Dataheap_VideoGrabber_001_search_01(self):
        """Test 'search' method from MythTV.VideoGrabber
           using 'searchVideos'.
        """
        from MythTV import MythDB, RecordedArtwork, Video, VideoGrabber

        with add_log_flags():
            self.mydb =  MythDB()

            title      = self.testenv['VIDTITLE']
            cast       = self.testenv['VIDCAST']
            inetrefstr = self.testenv['VIDINETREF']
            lang       = self.testenv['VIDLANGUAGE']

            # remove grabber from inetref:
            try:
                inetref = inetrefstr.split('_')[-1]
            except IndexError:
                inetref = inetrefstr

            vids = self.mydb.searchVideos( title = title )
            vid = next(vids)
            # print("%s : %s" %(vid.title, type(vid.title)))
            self.assertTrue(isinstance(vid, Video))
            grab = VideoGrabber("Movie", lang = lang, db = self.mydb)
            metadatalistgen = grab.search(vid.title, subtitle=None, tolerance=1)
            mlist = list(metadatalistgen)
            inetref_found = False
            for m in mlist:
                if (m.inetref == inetref):
                    inetref_found = True
                    break
            self.assertTrue(inetref_found)


    def test_Dataheap_VideoGrabber_001_grabInetref_01(self):
        """Test 'grabInetref' and 'toXML' methods from MythTV.VideoGrabber
           using predefined  values.
        """
        from MythTV import MythDB, RecordedArtwork, Video, VideoGrabber

        with add_log_flags():
            self.mydb =  MythDB()

            title      = self.testenv['VIDTITLE_DE']
            cast       = self.testenv['VIDCAST_DE']
            inetrefstr = self.testenv['VIDINETREF_DE']
            lang       = self.testenv['VIDLANGUAGE_DE']

            # remove grabber from inetref:
            try:
                inetref = inetrefstr.split('_')[-1]
            except IndexError:
                inetref = inetrefstr

            grab = VideoGrabber("Movie", lang=lang, db=self.mydb)
            metadatalist = grab.sortedSearch(title, subtitle=None, tolerance=2)

            details = grab.grabInetref(metadatalist[0].inetref)
            # details has lists of dicts for
            #  'certifications',  'categories', 'countries', 'studios', 'people', 'images'

            names = [n.name for n in details.people]
            self.assertTrue(cast in names)

            tree  = etree.XML(u'<metadata></metadata>')
            tree.append(details.toXML())
            xml_str = etree.tostring ( tree
                                     , pretty_print    = True
                                     , xml_declaration = True
                                     , encoding        = "UTF-8"
                                     , standalone      = "yes"
                                     )
            xml_file  = open("/tmp/details.xml", "wb")
            xml_file.write(xml_str)
            xml_file.close()

            # read xml file and check for cast
            root = etree.parse(r'/tmp/details.xml').getroot()
            cast_found = False
            for name in root.findall('item/people/person'):
                if (name.attrib['name'] == cast):
                    cast_found = True
            self.assertTrue(cast_found)


class test_Dataheap_VideoGrabber_002(unittest.TestCase):
    """Test class 'VideoGrabber' from dataheap.
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv
        # moke INSTALL_PREFIX
        global INSTALL_PREFIX
        cls.INSTALL_PREFIX = INSTALL_PREFIX
        # clear 'pytmdb3.cache'
        pytmdb3_cache = os.path.expanduser('~/.mythtv/cache/pytmdb3.cache')
        if os.path.exists(pytmdb3_cache):
            os.remove(pytmdb3_cache)

    def setUp(self):
        # check INSTALL_PREFIX
        if (self.INSTALL_PREFIX != os.getcwd()):
            self.fail("Unable to rewrite 'INSTALL_PREFIX' in static.py!")

    def tearDown(self):
        if os.path.exists("/tmp/my_logfile"):
            os.remove("/tmp/my_logfile")
        if os.path.exists("/tmp/details.xml"):
            os.remove("/tmp/details.xml")

    def is_sublist(self, list1, list2):
       ls1 = [element for element in list1 if element in list2]
       ls2 = [element for element in list2 if element in list1]
       return ls1 == ls2


    def test_Dataheap_VideoGrabber_002_importMetadata_01(self):
        """Test 'VideoGrabber.grabInetref' method and 'Video.importMetadata'
           methods using predefined values. See 'mythvidexport.py' as well.
           See MythtTV trac tickets #12243 and #12245.
           Note: Use a video with French accents in title and cast.
        """
        from MythTV import MythDB, Video, VideoGrabber

        with add_log_flags():

            title      = u"Le Dernier Métro"
            castlist   = [u"Catherine Deneuve", u"Gérard Depardieu", u"Andréa Ferréol"]
            inetstr    = "tmdb3.py_1716"
            lang       = "fr"
            filename   = title + u".mkv"

            # create a new Video instance
            self.mydb = MythDB()
            vid  = Video(db=self.mydb).create ({'title'   : title,
                                                'filename': filename,
                                                'host'    : self.mydb.getMasterBackend()})
            # grab details from www.themoviedb.org
            grab = VideoGrabber('MOVIE', lang=lang, db=self.mydb)
            metadata = grab.grabInetref(inetstr)
            #print(type(metadata))   -->   <class 'MythTV.system.VideoMetadata'>
            # import metadata into Video instance
            vid.importMetadata(metadata)
            #print(vid.cast[1].cast)   ### --->  Gérard Depardieu
            # create a list of cast members from metadata
            vidcastmembers = [c.cast for c in vid.cast]
            # check for members in cast list
            self.assertTrue(self.is_sublist(castlist, vidcastmembers))
            # delete previously created Video object in database
            vid.delete()
            #print(metadata.inetref)   # --> 1716
            self.assertEqual(metadata.inetref, inetstr.split('_')[-1])
            # run the grabber again, but based on a 'VideoMetadata' object
            new_metadata = grab.grabInetref(metadata)
            # check if collected metadata are the equal
            self.assertEqual(new_metadata, metadata)

    def test_Dataheap_VideoGrabber_002_importMetadata_02(self):
        """Test 'VideoGrabber.grabInetref' method and 'Video.importMetadata'
           methods using predefined values. See 'mythvidexport.py' as well.
           See MythtTV trac tickets #12243 and #12245.
           Note: Use a TV series with season and episode.
        """
        from MythTV import MythDB, Video, VideoGrabber

        with add_log_flags():
            self.mydb =  MythDB()

            alf_metadata = { u'title'    : u'Alf',
                             u'subtitle' : u'Wedding Bell Blues',
                             u'season'   : 2,
                             u'episode'  : 4,
                             u'inetref'  : '78020'}

            grab = VideoGrabber('TV', lang='en', db=self.mydb)
            metadata = grab.grabInetref( alf_metadata['inetref'],
                                         alf_metadata['season'],
                                         alf_metadata['episode'])

            # print(metadata.collectionref)   # ---> '78020'
            self.assertEqual(metadata.collectionref, alf_metadata[u'inetref'])

            # run the grabber again, but based on a 'VideoMetadata' object
            new_metadata = grab.grabInetref(metadata)
            # check if collected metadata are the equal
            self.assertEqual(new_metadata, metadata)

if __name__ == '__main__':
    unittest.main()
