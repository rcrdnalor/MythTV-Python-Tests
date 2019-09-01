# -*- coding: utf-8 -*-

import unittest


from MythTV import MythDB, DBData, Recorded, OldRecorded, RecordedArtwork, Job, Guide, Record,\
     Video, System, Program, MythBE, Frontend, Channel, MythError, MythDBError, MythFEError, datetime


from test.helpers import get_test_env

# globals:
TestEnv = {}

def setUpModule():
    """called once, before anything else in this module"""
    # pull in test environment as dict
    global TestEnv
    get_test_env(TestEnv)

class test_repr_and_str_001(unittest.TestCase):
    """
    Test '__repr__' and '__str__' methods from MythTV.
    File: database.py
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv


    def test_repr_001_01(self):
        """
        Test '__repr__' and '__str__' methods from MythTV.MythDB.
        This testcase shows a good example how mysql tables are handled within
        the MythTV Python Bindings.
        """

        # how to interface with a mysql table from mythconverg:
        #  create a class or use an existing one that uses the
        #  tables from MythTv's database inside 'mythconverg:
        class RecGroup(DBData):
            """
            RecGroup(data=None, db=None) --> Recgroup object to
            database table 'recgroups', data is a `recgroup` string.

            - get information about the table:
              $ mysql -h <master-backend-ip> -u mythtv -p<password-from-config.xml> mythconverg

              MariaDB [mythconverg]> describe recgroups;
                +-------------+-------------+------+-----+---------+----------------+
                | Field       | Type        | Null | Key | Default | Extra          |
                +-------------+-------------+------+-----+---------+----------------+
                | recgroupid  | smallint(4) | NO   | PRI | NULL    | auto_increment |
                | recgroup    | varchar(64) | NO   | UNI |         |                |
                | displayname | varchar(64) | NO   |     |         |                |
                | password    | varchar(40) | NO   |     |         |                |
                | special     | tinyint(1)  | NO   |     | 0       |                |
                +-------------+-------------+------+-----+---------+----------------+
                5 rows in set (0.00 sec)


            Note: This class uses the init from its parent (DBData),
                  __repr__ and __str__ are inherited from DBData, too.


            """
            _table = 'recgroups'
            _key   = ['recgroup']

            # thats all for reading the mysql tables, everything is done!


        # connect to the database:
        db = MythDB()
        # - for unittest only: test database connection
        __trepr = repr(db)
        __tstr  = str(db)
        print()
        print(__trepr)
        print(__tstr)
        self.assertTrue(u'mythconverg@' in __tstr)

        # instantiate (i.e.: call) the class with meaningful values
        rgroup = RecGroup(u'LiveTV', db=db)

        # look at the fields of the table:
        tf = db.tablefields
        # - for unittest only: test 'db.tablefields'
        print()
        print(repr(tf))
        print(str(tf))
        # this shows "['recgroups']", therfore explore them
        print()
        print(repr(db.tablefields.recgroups.recgroup))
        print(str(db.tablefields.recgroups.recgroup))



    def test_repr_001_02(self):
        """
        Test '__repr__' and '__str__' methods from MythTV.MythDB.settings
        """

        db = MythDB()
        s = db.settings
        print()
        print(repr(s))
        print(str(s))
        #self.assertTrue(u'DBSchemaVer' in str(s))

        sn = db.settings['NULL']
        print()
        print(repr(sn))
        print(str(sn))

        ip = db.settings.NULL.MasterServerIP
        print()
        print(repr(ip))
        print(str(ip))

        fn = db.settings['%s' %self.testenv['FRONTENDNAME']]
        print()
        print(repr(fn))
        print(str(fn))

        fnp  = fn.NetworkControlPort
        print()
        print(repr(fnp))
        print(str(fnp))


    def test_repr_001_03(self):
        """
        Test '__repr__' and '__str__' methods from MythTV.MythDB.StorageGroup
        """

        db = MythDB()

        sgi = db.getStorageGroup('LiveTV')
        sg = next(sgi)
        print()
        print(repr(sg))
        print(str(sg))


class test_repr_and_str_002(unittest.TestCase):
    """
    Test '__repr__' and '__str__' methods from MythTV.
    File: dataheap.py
    File: mythproto.py (partial)
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def test_repr_002_01(self):
        """
        Test '__repr__' and '__str__' methods from dataheap.py
        """

        chanid        = self.testenv['RECCHANID']
        starttimemyth = self.testenv['RECSTARTTIMEMYTH']
        title         = self.testenv['RECTITLE']

        c_s = (chanid, starttimemyth)

        db = MythDB()
        # Recorded class
        r = Recorded(c_s, db=db)
        print()
        print(repr(r))
        print(str(r))

        # Markup table
        m = r.markup
        print()
        print(repr(m))
        print(str(m))
        # one entry of the marlup table:
        print()
        print(repr(m[0]))
        print(str(m[0]))
        # one value of a single entry:
        print()
        print(repr(m[0].mark))
        print(str(m[0].mark))
        print()
        print(repr(m[0].data))
        print(str(m[0].data))

        # Artwork
        a = r.artwork
        print()
        print(repr(a))
        print(str(a))

        # Coverart of an Artwork
        ac = a.coverart
        print()
        print(repr(ac))
        print(str(ac))

        # Program of the recorded entry:
        prgrm = r.getRecordedProgram()
        print()
        print(repr(prgrm))
        print(str(prgrm))

        # OldRecorded of the recorded entry:
        oldrecs = db.searchOldRecorded( chanid = chanid, title  = title )
        oldrec  = next(oldrecs)
        print()
        print(repr(oldrec))
        print(str(oldrec))


    def test_repr_002_02(self):
        """
        Test '__repr__' and '__str__' methods from dataheap.py
        """

        # Channel object:
        db = MythDB()
        c = Channel(self.testenv['RECCHANID'], db)
        print()
        print(repr(c))
        print(str(c))
        # 'visible' property of that channel:
        v = c.visible
        print()
        print(repr(v))
        print(str(v))


class test_repr_and_str_003(unittest.TestCase):
    """
    Test '__repr__' and '__str__' methods from MythTV.
    File: methodheap.py
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def test_repr_003_01(self):
        """
        Test '__repr__' and '__str__' methods of 'Frontend' class.
        """

        db = MythDB()

        fe = Frontend("%s" %(self.testenv['FRONTENDIP']), 6546)
        print()
        print(repr(fe))
        print(str(fe))

        # print list of keys and jump values
        print()
        print(repr(fe.key))
        print(str(fe.key))
        print()
        print(repr(fe.jump))
        print(str(fe.jump))


class test_repr_and_str_004(unittest.TestCase):
    """
    Test '__repr__' and '__str__' methods from MythTV.
    File: mythproto.py
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def test_repr_004_01(self):
        """
        Test '__repr__' and '__str__' methods of 'MythBE' class.
        Note: MythBE inherits from 'FileOps', which is inherited from 'BeCache'.
        """

        db = MythDB()
        be = MythBE(db=db)
        print()
        print(repr(be))
        print(str(be))


class test_repr_and_str_005(unittest.TestCase):
    """
    Test '__repr__' and '__str__' methods from MythTV.
    File: system.py
    """

    @classmethod
    def setUpClass(cls):
        # get the global test environment
        global TestEnv
        cls.testenv = TestEnv

    def test_repr_005_01(self):
        """
        Test '__repr__' and '__str__' methods of 'MythBE' class.
        Note: MythBE inherits from 'FileOps', which is inherited from 'BeCache'.
        """

        s = System(path='echo')
        print()
        print(repr(s))
        print(str(s))

if __name__ == '__main__':
    unittest.main()
