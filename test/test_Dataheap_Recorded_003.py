# -*- coding: UTF-8 -*-


import unittest

import os, sys

from MythTV import MythDB, Recorded, DBDataWrite

from test.helpers import get_test_env, add_log_flags

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)


class test_Dataheap_Recorded_003(unittest.TestCase):
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


    def test_Dataheap_Recorded_003_01(self):
        """Test creation of a Recoreded and
           writing/reading to the 'recordedcredits' table.
           it tests the entries of the 'people' table as well.
           UUT: class DBDataCRef
        """

        class People(DBDataWrite):
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

            _defaults = {u'name' : ''}

            ### end class People


        # a recording with french accents in the cast

        title         = self.testenv['RECFRTITLE']     # "Le Dernier Métro", "Die letzte Metro"
        chanid        = self.testenv['RECFRCHANID']
        starttimemyth = self.testenv['RECFRSTARTTIMEMYTH']

        #print(title)

        castlist = [ (u'Catherine Deneuve', u'actor'   )
                   , (u"Gérard Depardieu",  u'actor'   )
                   , (u"Andréa Ferréol",    u'actor'   )
                   , (u"Jean Poiret", 'actor')
                   , (u"François Truffaut", u'director')
                   ]

        # ensure, that "Jean Poiret" is already in the 'people' table
        try:
            p = People(u"Jean Poiret", db = self.mydb)
        except:
            p = People(db = self.mydb).create( {'name' : u"Jean Poiret"} )
            p.update()

        # get a recording, search for the title
        recs = self.mydb.searchRecorded(title = title)
        rec = next(recs)
        self.assertEqual(rec.chanid, int(chanid))

        # backup the cast of this recording
        org_cast = rec.cast

        # add castlist to cast
        for c in castlist:
            rec.cast.add(*c)             # need to de-reference the tuple
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

        p.delete()
        p.update()

if __name__ == '__main__':
    unittest.main()


