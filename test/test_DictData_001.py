# -*- coding: utf-8 -*-

import unittest
import sys
import os
import pickle

from MythTV import DictData
from MythTV import datetime
from datetime import date



class My_DictData(DictData):
    _localvars = ['_field_order', 'UnKnown']

    _field_order = [ 'field_a'  # integer
                   , 'field_b'  # float
                   , 'field_c'  # bool
                   , 'field_d'  # x
                   , 'field_e'  # fromtimestamp
                   , 'field_f'  # ISO date
                   , 'field_g'  # RFC time
                   , 'field_h'  # float
                   , 'field_i'  # bool
                   , 'field_j'  # bool
                   , 'field_k'  # bool
                   , 'field_l'  # bool
                   , 'field_m'  # str
                   ]

    _field_type =  [  0         # integer
                   ,  1         # float
                   ,  2         # bool
                   ,  3         # x
                   ,  4         # fromtimestamp
                   ,  5         # ISO date
                   ,  6         # RFC time
                   ,  1         # float
                   ,  2         # bool
                   ,  2         # bool
                   ,  2         # bool
                   ,  2         # bool
                   ,  3
                   ]


class My_DictData_Pass_Through(DictData):
    _field_order = [ 'field_a'  # integer
                   , 'field_b'  # float
                   , 'field_c'  # bool
                   , 'field_d'  # x
                   , 'field_e'  # fromtimestamp
                   , 'field_f'  # ISO date
                   , 'field_g'  # RFC time
                   , 'field_h'  # float
                   , 'field_i'  # bool
                   , 'field_j'  # bool
                   , 'field_k'  # bool
                   , 'field_l'  # bool
                   , 'field_m'  # str
                   ]

    _field_type = 'Pass'


class test_DictData_001(unittest.TestCase):
    """Test basic DictData functionality of MythTV.altdict."""


    @classmethod
    def setUpClass(cls):
        cls.field_values =  [ '4711'                        # integer
                            , '1234.4567'                   # float
                            , '1'                           # bool
                            , 'Thank you for the fish'      # x
                            , '1558110396'                  # fromtimestamp
                            , '2019-01-01'                  # ISO date
                            , 'Wed, 27 Feb 2013 17:18:15'   # RFC time
                            , '9.8765'                      # float
                            , '0'                           # bool
                            , '1'                           # bool
                            , 0                             # bool
                            , 1                             # bool
                            , ''
                            ]


        cls.my_dict_data = My_DictData(cls.field_values)
        cls.org_values   = cls.my_dict_data._deprocess()

        # read and set a value
        fk = cls.my_dict_data['field_k']
        fl = cls.my_dict_data.field_l
        cls.my_dict_data['field_k'] = fl
        cls.my_dict_data.field_l = fk
        cls.my_dict_data['field_k'] = fk
        cls.my_dict_data.field_l = fl

        cls.my_dict_data_pass_through = My_DictData_Pass_Through(cls.field_values)
        cls.org_values_pass_through   = cls.my_dict_data_pass_through._deprocess()


    def test_dictdata_001_00(self):
        """Test copy of the DictData."""
        ddc = self.my_dict_data.copy()
        self.assertTrue(isinstance(ddc, DictData))
        self.assertTrue(id(self.my_dict_data._localvars), id(ddc._localvars))
        ddc._fillNone()
        self.assertTrue(ddc['field_d'] == None)


    def test_dictdata_001_01(self):
        """Test filling and 'decompressing' of a simple DictData 'integer' object."""

        # field_a, integer, '4711'
        self.assertEqual(self.org_values[0], self.field_values[0])
        self.assertEqual(type(self.org_values[0]), type(self.field_values[0]))
        self.assertTrue(isinstance(self.my_dict_data.field_a, int))


    def test_dictdata_001_02(self):
        """Test filling and 'decompressing' of a simple DictData 'float' object."""

        # field_b, float, '1234.4567'
        self.assertTrue(self.org_values[1].startswith(self.field_values[1]))
        self.assertEqual(type(self.org_values[1]), type(self.field_values[1]))
        self.assertTrue(isinstance(self.my_dict_data.field_b, float))

        # field_h, float, '9.8765'
        self.assertTrue(self.org_values[7].startswith(self.field_values[7]))
        self.assertEqual(type(self.org_values[7]), type(self.field_values[7]))
        self.assertTrue(isinstance(self.my_dict_data.field_h, float))


    def test_dictdata_001_03(self):
        """Test filling and 'decompressing' of a simple DictData 'bool' object."""

        # field_i, bool, '0' : '0' --> bool(0) --> '0', works
        self.assertEqual(self.org_values[8], self.field_values[8])
        self.assertEqual(type(self.org_values[8]), type(self.field_values[8]))
        self.assertTrue(isinstance(self.my_dict_data.field_i, bool))

        # field_j, bool, '1' : '1' --> bool(1) --> '1', works
        self.assertEqual(self.org_values[9], self.field_values[9])
        self.assertEqual(type(self.org_values[9]), type(self.field_values[9]))
        self.assertTrue(isinstance(self.my_dict_data.field_j, bool))

        # field_k, bool, 0 : 0 --> bool(0) --> '0', does not work
        self.assertNotEqual(self.org_values[10], self.field_values[10])
        self.assertNotEqual(type(self.org_values[10]), type(self.field_values[10]))
        self.assertTrue(isinstance(self.my_dict_data.field_k, bool))

        # field_l, bool, 1: 1 --> bool(1) --> '1', does not work
        self.assertNotEqual(self.org_values[11], self.field_values[11])
        self.assertNotEqual(type(self.org_values[11]), type(self.field_values[11]))
        self.assertTrue(isinstance(self.my_dict_data.field_l, bool))


    def test_dictdata_001_04(self):
        """Test filling and 'decompressing' of a simple DictData 'str' object."""

        # field_d, str, 'Thank you for the fish'
        self.assertEqual(self.org_values[3], self.field_values[3])
        self.assertEqual(type(self.org_values[3]), type(self.field_values[3]))
        self.assertTrue(isinstance(self.my_dict_data.field_d, str))


    def test_dictdata_001_05(self):
        """Test filling and 'decompressing' of a simple DictData 'tiemstamp' object."""

        # field_e, timestamp, '1558110396'
        self.assertEqual(self.org_values[4], self.field_values[4])
        self.assertEqual(type(self.org_values[4]), type(self.field_values[4]))
        self.assertTrue(isinstance(self.my_dict_data.field_e, datetime))


    def test_dictdata_001_06(self):
        """Test filling and 'decompressing' of a simple DictData 'ISO date' object."""

        # field_f, ISO date, '2019-01-01'
        self.assertEqual(self.org_values[5], self.field_values[5])
        self.assertEqual(type(self.org_values[5]), type(self.field_values[5]))
        self.assertTrue(isinstance(self.my_dict_data.field_f, date))


    def test_dictdata_001_07(self):
        """Test filling and 'decompressing' of a simple DictData 'RFC time' object."""

        # field_g, RFC time, 'Wed, 27 Feb 2013 17:18:15'
        self.assertEqual(self.org_values[6], self.field_values[6])
        self.assertEqual(type(self.org_values[6]), type(self.field_values[6]))
        self.assertTrue(isinstance(self.my_dict_data.field_g, datetime))

    def test_dictdata_001_08(self):
        """Test exception in '__setitem__' for unknown key."""
        with self.assertRaises(KeyError) as context:
            self.my_dict_data['unknown'] = True
        self.assertTrue('unknown' in str(context.exception))


    def test_dictdata_001_09(self):
        """Test setting of an unknown key (var 1)."""
        #self.my_dict_data._field_order.append('UnKnown')
        self.my_dict_data.UnKnown = False
        self.assertFalse(self.my_dict_data.UnKnown)
        self.assertFalse(self.my_dict_data.UnKnown in self.my_dict_data.keys())
        self.my_dict_data.NotKnown = True
        self.assertTrue(self.my_dict_data.NotKnown)
        self.assertFalse(self.my_dict_data.NotKnown in self.my_dict_data.keys())


    def test_dictdata_001_10(self):
        """Test setting an unknown key (var 2)."""
        ukey = 100
        self.my_dict_data._field_order.append(ukey)
        # print(self.my_dict_data._field_order[-1])
        with self.assertRaises(AttributeError) as context:
            self.my_dict_data.__setattr__((ukey.lower()), 'blah')
        # print(str(context.exception))
        self.my_dict_data._field_order = self.my_dict_data._field_order[: -1]
        self.assertTrue('lower' in str(context.exception))


    def test_dictdata_001_11(self):
        """Test deleting a key (var 1)."""
        with self.assertRaises(NotImplementedError) as context:
            del self.my_dict_data['field_d']
            self.assertTrue('field_d' in str(context.exception))


    def test_dictdata_001_12(self):
        """Test deleting a key (var 2)."""
        del self.my_dict_data.UnKnown
        self.assertFalse('UnKnown' in self.my_dict_data.__dict__)


    def test_dictdata_001_13(self):
        """Test deleting a key (var 3)."""
        with self.assertRaises(AttributeError) as context:
            del self.my_dict_data.WellKnown
        self.assertTrue('WellKnown' in str(context.exception))


    def test_dictdata_001_14(self):
        """Test unequal length."""
        with self.assertRaises(Exception) as context:
            self.field_values.append(42)
            ddc = My_DictData(self.field_values)
        self.assertTrue('Incorrect raw input length' in str(context.exception))


    def test_dictdata_001_15(self):
        """Test passthrough of field_type."""
        self.assertTrue(self.my_dict_data_pass_through.field_b == self.field_values[1])
        self.assertTrue(self.org_values_pass_through[1] == self.field_values[1])

        self.my_dict_data_pass_through.field_b = 'beta'
        self.assertTrue(self.my_dict_data_pass_through.field_b == 'beta')


#    def test_dictdata_001_16(self):
#        """ Test pickle and unpickle of DictData."""
#        with open('test.pkl','wb') as fw:
#            pickle.dump(self.my_dict_data, fw)
#        with open('test.pkl', 'rb') as fr:
#            pdd = pickle.load(fr)
#        self.assertTrue(self.field_values[1].startswith(str(pdd.field_b)))
#        self.assertTrue(isinstance(pdd.field_b, float))
#        org_pdd = pdd._deprocess()
#        self.assertTrue(isinstance(org_pdd[1], str))


if __name__ == '__main__':
    unittest.main()

