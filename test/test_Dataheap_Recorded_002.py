# -*- coding: UTF-8 -*-


import unittest

import os, sys

from MythTV import MythDB, Recorded, DBData

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Recorded_002(unittest.TestCase):
    """Test creation of a Recoreded and
       writing/reading to the 'recordedrating' table.
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


    def test_Dataheap_Recorded_002_01(self):
        """Test creation of a Recoreded and
           writing/reading to the 'recordedrating' table.
           UUT: class DBDataRef
           Caution: recn.update() does not delete a removed entry from the 'recordedrating' table !
           Only recn.rating.clean() removes all entries.
        """

        chanid        = self.testenv['DOWNCHANID']
        starttimemyth = self.testenv['DOWNSTARTTIME']

        rec = Recorded((chanid, starttimemyth), db=self.mydb)

        # Recorded.rating is a list of lists of tuples
        # [[(u'system', u'ABCD'), (u'rating', '08.15')], [(u'system', u'WXYZ'), (u'rating', u'0.11')]]

        # add ratings to the recorded instance:
        rec.rating.add(u'ABCD', u'41.98')
        rec.rating.add(u'WXYZ', u'0.11')

        # check the ratings:
        #print(rec.rating)
        s0_found = s1_found = False
        r0_found = r1_found = False
        for (s,r) in rec.rating:
            # print(s)
            # print(r)
            if s == u'ABCD':
                s0_found = True
            if s == u'WXYZ':
                s1_found = True
            if r == u'41.98':
                r0_found = True
            if r ==  u'0.11':
                r1_found = True
        self.assertTrue(s0_found)
        self.assertTrue(s1_found)
        self.assertTrue(r0_found)
        self.assertTrue(r1_found)

        # revert last changes:
        rec.rating.revert()
        # check for an empty list:
        #print(rec.rating)
        self.assertEqual(len(rec.rating), 0)

        # add ratings again:
        rec.rating.add('ABCD', '41.98')
        rec.rating.add('QWERTZ', 'blah')
        rec.rating.add('WXYZ', '0.11')
        # commit these updates:
        rec.update()

        # get the recorded data again:
        recn = Recorded((chanid, starttimemyth), db=self.mydb)
        # edit existing rating data:
        for i,(s,r) in enumerate(recn.rating):
            if s == 'ABCD':
               break
        if i is not None:
            recn.rating[i]['rating'] = u'08.15'
        # commit that change:
        recn.update()
        # check the changed value:
        #print(rec.rating)
        rn_found = False
        for (s,r) in recn.rating:
            if r == u'08.15':
                rn_found = True
        self.assertTrue(rn_found)

        # delete a rating:
        recn.rating.delete(u'WXYZ', u'0.11')
        recn.update()
        #print(recn.rating)
        sn_found = False
        for (s,r) in recn.rating:
            if s == u'WXYZ':
                sn_found = True
        self.assertFalse(sn_found)

        # clean all ratings for this recorded instance:
        recn.rating.clean()
        recn.update()
        self.assertEqual(len(recn.rating), 0)


    def test_Dataheap_Recorded_002_02(self):
        """Test creation of a Recoreded and
           writing/reading to the 'recordedcredits' table.
           it tests the entries of the 'people' table as well.
           UUT: class DBDataCRef
        """

        """
        $ python - --nodblog --loglevel debug --verbose all --logfile /tmp/my_logfile
        Python 2.7.15+ (default, Oct  7 2019, 17:39:04)
        [GCC 7.4.0] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from MythTV import MythDB, Video, Recorded
        >>> d = MythDB()
        _initlogger call
        _parseinput call
        >>> rec =d.searchRecorded(title = 'Die letzte Metro')
        >>> r = next(rec)
        >>> r
        b'<Recorded 'Die letzte Metro','2014-10-16 22:16:00+02:00' at 0x7f96bde242a0>'
        >>> r.cast
        []
        >>> r.cast._refdat
        [11301L, datetime(2014, 10, 16, 20, 18, 21)]
        >>> r.cast._datfields
        [u'name', u'role']

        >>> r.cast.add('Catherine Deneuve', 'actor')
        >>> r.cast
        [[(u'name', 'Catherine Deneuve'), (u'role', 'actor')]]
        >>> r.cast.add(u"Gérard Depardieu", 'actor')
        >>> r.cast.add(u"Andréa Ferréol", 'actor')
        >>> r.cast.add(u"François Truffaut", 'director')
        >>> r.cast
        [[(u'name', 'Catherine Deneuve'), (u'role', 'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', 'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', 'actor')], [(u'name', u'Fran\xe7ois Truffaut'), (u'role', 'director')]]
        >>> r.update()

        >>> print(r.cast[1]['name'])
        Gérard Depardieu


        >>> r.cast.add(u"Jean Poiret", 'actor')
        >>> r.cast.add(u"Jean-Louis Richard", 'actor')
        >>> r.cast
        [[(u'name', 'Catherine Deneuve'), (u'role', 'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', 'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', 'actor')], [(u'name', u'Fran\xe7ois Truffaut'), (u'role', 'director')], [(u'name', u'Jean Poiret'), (u'role', 'actor')], [(u'name', u'Jean-Louis Richard'), (u'role', 'actor')]]
        >>> r.update()


        >>> r1 = Recorded((r.chanid, r.starttime), db =d)
        >>> r1
        b'<Recorded 'Die letzte Metro','2014-10-16 22:16:00+02:00' at 0x7f96bde2d868>'
        >>> r1.cast
        [[(u'name', u'Catherine Deneuve'), (u'role', u'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', u'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', u'actor')], [(u'name', u'Fran\xe7ois Truffaut'), (u'role', u'director')], [(u'name', u'Jean Poiret'), (u'role', u'actor')], [(u'name', u'Jean-Louis Richard'), (u'role', u'actor')]]
        >>> r1.cast.delete(u'Jean-Louis Richard', u'actor')
        >>> r1.cast
        [[(u'name', u'Catherine Deneuve'), (u'role', u'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', u'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', u'actor')], [(u'name', u'Fran\xe7ois Truffaut'), (u'role', u'director')], [(u'name', u'Jean Poiret'), (u'role', u'actor')]]
        >>> r1.update()
        >>> r1.cast
        [[(u'name', u'Catherine Deneuve'), (u'role', u'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', u'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', u'actor')], [(u'name', u'Fran\xe7ois Truffaut'), (u'role', u'director')], [(u'name', u'Jean Poiret'), (u'role', u'actor')]]


        Attention: Recorded.cast.delete() deletes the entries in the 'people' table as well !!

        >>> r1.cast.delete(u"Jean Poiret", 'actor')
        >>> r1.update()
        >>> r1.cast.delete(u"François Truffaut", 'director')
        >>> r1.update()
        >>> r1.cast
        [[(u'name', u'Catherine Deneuve'), (u'role', u'actor')], [(u'name', u'G\xe9rard Depardieu'), (u'role', u'actor')], [(u'name', u'Andr\xe9a Ferr\xe9ol'), (u'role', u'actor')]]


        """

        class People(DBData):
            """
            People(data=None, db=None) --> People object to
            database table 'people', data is a `name` string.

            - get information about the table:
              $ mysql -h <master-backend-ip> -u mythtv -p<password-from-config.xml> mythconverg

              MariaDB [mythconverg]> describe people;
                +-------------+-----------------------+------+-----+---------+----------------+
                | Field       | Type                  | Null | Key | Default | Extra          |
                +-------------+-----------------------+------+-----+---------+----------------+
                | person      | mediumint(8) unsigned | NO   | PRI | NULL    | auto_increment |
                | name        | varchar(128)          | NO   | UNI |         |                |
                +-------------+-----------------------+------+-----+---------+----------------+
                2 rows in set (0.00 sec)

            """
            _table = 'people'
            _key   = ['name']

            ### end class Person


        # a recording with french accents in the cast

        title         = self.testenv['RECFRTITLE']     # "Le Dernier Métro"
        chanid        = self.testenv['RECFRCHANID']
        starttimemyth = self.testenv['RECFRSTARTTIMEMYTH']

        print(title)

        castlist = [ (u'Catherine Deneuve', u'actor'   )
                   , (u"Gérard Depardieu",  u'actor'   )
                   , (u"Andréa Ferréol",    u'actor'   )
                   , (u"François Truffaut", u'director')
                   ]

        # get a recording, search for the title
        recs = self.mydb.searchRecorded(title = title)
        rec = next(recs)
        self.assertEqual(rec.chanid, int(chanid))

        # backup the cast of this recording
        org_cast = rec.cast

#         ## backup the people table
#         #org_people = People(db=self.mydb)

#         # check if entries in castlist does not occur in cast
#         for name,role in castlist:
#             print(name)
#             print(role)

# #            if  in rec.cast:
# #                rec.cast.delete(*c)      # need to dereference the tuple
#         sys.exit(1)
#         rec.update()
#         # remember length
#         cast_length = len(rec.cast)
#         # check if the members of the cast are listed
#         # in the 'people' table
#         cast_found = False
#         for c in castlist:
#             try:
#                 cname = People(c[0])
#                 cast_found = True
#             except:
#                 pass
#         # cast should no be listed in the people table
#         self.assertFalse(cast_found)

        # add castlist to cast
        for c in castlist:
            rec.cast.add(*c)             # need to dereference the tuple
        print(rec.cast)
        #sys.exit(1)
        rec.update()

        # check again if the members of the cast are listed
        # in the 'people' table
        cast_found = False
        for c in castlist:
            try:
                cname = People(c[0])
                cast_found = True
            except:
                pass
        # now cast should be listed in the people table
        self.assertTrue(cast_found)

        # get the len of the rec.casts
        c1_length = len(rec.cast)
        # delete on entry
        rec.cast.delete(*castlist[2])
        rec.update()
        self.assertEqual(c1_length -1, len(rec.cast))

        # delete all entries
        rec.cast.clean()  # this does a commit as well
        self.assertEqual(len(rec.cast), 0)

        # add the previously saved cast back
        # to a new instance of that recording
        recn = Recorded((rec.chanid, rec.starttime), db = self.mydb)
        for cs in org_cast:
            recn.cast.add(cs)
        recn.update

        self.assertEqual(len(recn.cast), len(org_cast))

if __name__ == '__main__':
    unittest.main()


