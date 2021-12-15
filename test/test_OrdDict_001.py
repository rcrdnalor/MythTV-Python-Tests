# -*- coding: utf-8 -*-

import unittest
import sys
import os
import pickle
from collections.abc import Iterable

from MythTV.altdict import OrdDict


class test_OrdDict_001(unittest.TestCase):
    """Test basic OrdDict functionality of MythTV.altdict."""

    @classmethod
    def setUpClass(cls):
        cls.field_values =  [ '4711'
                            , '1234.4567'
                            , '1'
                            , 'Thank you for the fish'
                            ]
        cls.field_keys = [ 'field_a'
                         , 'field_b'
                         , 'field_c'
                         , 'field_d'
                         ]
        cls.my_ord_dict = OrdDict(zip(cls.field_keys, cls.field_values))


    def test_OrdDict_001_00(self):
        """Test equality and order of OrdDict."""
        my_test_dict1 = OrdDict()
        my_test_dict1['field_a'] = '4711'
        my_test_dict1['field_b'] = '1234.4567'
        my_test_dict1['field_c'] = '1'
        my_test_dict1['field_d'] = 'Thank you for the fish'
        self.assertEqual(self.my_ord_dict, my_test_dict1)

        my_test_dict2 = OrdDict()
        my_test_dict2['field_a'] = '1234.4567'
        my_test_dict2['field_b'] = '4711'
        my_test_dict2['field_c'] = '1'
        my_test_dict2['field_d'] = 'Thank you for the fish'
        self.assertNotEqual(self.my_ord_dict, my_test_dict2)

    def test_OrdDict_001_01(self):
        """Test getattr, getitem the OrdDict."""
        ak = self.my_ord_dict['field_a']
        aa = self.my_ord_dict.field_a
        self.assertTrue(ak == '4711')
        self.assertTrue(aa == '4711')

    def test_OrdDict_001_02(self):
        """Test setattr, setitem of the OrdDict."""
        self.my_ord_dict['field_a'] = '0815'
        self.my_ord_dict.field_b = 12.12
        self.assertTrue(self.my_ord_dict['field_a'] == '0815')
        self.assertTrue(self.my_ord_dict.field_b == 12.12)
        self.my_ord_dict['field_a'] = '4711'
        self.my_ord_dict.field_b = '1234.4567'

    def test_OrdDict_001_03(self):
        """Test setattr, getattr, delattr of local variables."""
        my_test_dict3 = OrdDict()
        my_test_dict3._localvars.append('dummy')
        my_test_dict3['field_a'] = '1234.4567'
        my_test_dict3['field_b'] = '4711'
        my_test_dict3['field_c'] = '1'
        my_test_dict3['field_d'] = 'Thank you for the fish'
        self.assertTrue('dummy' in my_test_dict3._localvars)
        my_test_dict3.dummy = 'd1'
        self.assertFalse('dummy' in my_test_dict3.keys())
        dummy_value = my_test_dict3.dummy
        self.assertTrue(dummy_value == 'd1')
        my_test_dict3.dummy = 'd2'
        dummy_value = my_test_dict3.dummy
        #print(my_test_dict3.__dict__)
        self.assertTrue(dummy_value == 'd2')
        self.assertTrue(dummy_value == my_test_dict3.__getattr__('dummy'))
        self.assertTrue('dummy' in my_test_dict3.__dict__.keys())
        del my_test_dict3.dummy
        self.assertFalse('dummy' in my_test_dict3.__dict__.keys())
        self.assertFalse('dummy' in my_test_dict3._field_order)

    def test_OrdDict_001_04(self):
        """Test delattr, delitem of the OrdDict."""
        my_test_dict4 = OrdDict()
        my_test_dict4['A'] = '4711'
        my_test_dict4['B'] = '4712'
        my_test_dict4['C'] = '4713'
        my_test_dict4['D'] = '4714'
        del my_test_dict4['C']
        del my_test_dict4.D
        self.assertFalse('C' in my_test_dict4.keys())
        self.assertFalse('D' in my_test_dict4.keys())

    def test_OrdDict_001_05(self):
        """Test iter of the OrdDict's values, items, keys."""
        ikeys = self.my_ord_dict.iterkeys()
        ivalues = self.my_ord_dict.itervalues()
        iitems = self.my_ord_dict.iteritems()
        self.assertTrue(isinstance(ikeys, Iterable))
        self.assertTrue(isinstance(ivalues, Iterable))
        self.assertTrue(isinstance(iitems, Iterable))
        self.assertTrue('field_c' in list(ikeys))
        self.assertTrue('1234.4567' in list(ivalues))
        self.assertTrue(('field_c', '1') in list(iitems))

    def test_OrdDict_001_06(self):
        """Test pickling of the OrdDict."""
        with open('test_ord_dict_01.pkl', 'wb') as fw:
            pickle.dump(self.my_ord_dict, fw)
        with open('test_ord_dict_01.pkl', 'rb') as fr:
            pod = pickle.load(fr)
        self.assertTrue(self.my_ord_dict == pod)
        pod.x = 'blah'
        self.assertFalse(pod == self.my_ord_dict)

    def test_OrdDict_001_07(self):
        """Test a copy of the OrdDict."""
        c = self.my_ord_dict.copy()
        self.assertEqual(c, self.my_ord_dict)
        self.assertEqual(c._localvars, self.my_ord_dict._localvars)

    def test_OrdDict_001_08(self):
        """Test 'self.values()' of the OrdDict."""
        values = self.my_ord_dict.values()
        self.assertEqual(list(values), self.field_values)

    def test_OrdDict_001_09(self):
        """Test 'self.clear()' of the OrdDict."""
        my_test_dict5 = OrdDict()
        my_test_dict5['A'] = '4711'
        my_test_dict5['B'] = '4712'
        my_test_dict5['C'] = '4713'
        my_test_dict5['D'] = '4714'
        my_test_dict5.clear()
        self.assertTrue('A' not in my_test_dict5)
        self.assertTrue(len(my_test_dict5) == 0)

    def test_OrdDict_001_10(self):
        """Test '__iter__' over OrdDict."""
        it = iter(self.my_ord_dict)
        k = next(it)
        self.assertTrue( k == self.field_values[0])
        k = next(it)
        k = next(it)
        self.assertTrue(k == self.field_values[2])
        with self.assertRaises(StopIteration) as context:
            k = next(it)
            k = next(it)
            k = next(it)
        self.assertTrue( k == self.field_values[-1])


if __name__ == '__main__':
    unittest.main()
