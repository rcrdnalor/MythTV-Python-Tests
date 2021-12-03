# -*- coding: utf-8 -*-

import unittest
import sys
from MythTV.altdict import DictInvert, DictInvertCI


field_values =  [ 'A'
                , 'B'
                , 'c'
                , 'd'
                ]
field_keys =    [ 'field_a'
                , 'field_b'
                , 1
                , 2
                ]

class test_DictInv_001(unittest.TestCase):

    def setUp(self):
        self.my_dict1 = dict(zip(field_keys, field_values))
        self.my_dict_inv_1 = DictInvert(self.my_dict1)
        field_valuesCI  = [x.lower() for x in field_values]
        self.my_dictCI = dict(zip(field_keys, field_valuesCI))
        self.dictA, self.dictB = DictInvertCI.createPair(self.my_dictCI)

    def tearDown(self):
        pass

    def test_DictInv_001_01(self):
        """Test '__setitem__', '__delitem__' of DictInvert."""
        self.my_dict_inv_1['E'] = 'field_e'
        self.assertTrue('E' in self.my_dict_inv_1)

        del self.my_dict_inv_1['E']
        self.assertFalse('E' in self.my_dict_inv_1)

        my_dict_inv_inv = DictInvert(self.my_dict_inv_1)
        self.assertTrue(my_dict_inv_inv == self.my_dict1)

    def test_DictInv_001_02(self):
        """Test 'createPair' of DictInvert."""
        dictX, dictZ = DictInvert.createPair({0:'none'})
        keyX = list(dictX.keys())[0]
        keyZ = list(dictZ.keys())[0]
        valX = list(dictX.values())[0]
        valZ = list(dictZ.values())[0]
        self.assertEqual(keyX, valZ)
        self.assertEqual(keyZ, valX)        
    
    def test_DictInv_001_03(self):
        """Test '__init__' with extra dict as argument."""
        my_dict0 = {'field_z': 'Z'}
        my_dict0_inv = DictInvert(self.my_dict1, my_dict0)
        self.assertTrue(my_dict0 == my_dict0_inv)

    def test_DictInvCI_001_01(self):
        """Test '__getitem__' of DictInvCI.""" 
        for i,k in enumerate(list(self.dictB.keys())):
            self.assertTrue(k == list(self.dictA.values())[i])

    def test_DictInvCI_001_02(self):
        """Test '__contains__' of DictInvCI.""" 
        for k in list(self.dictB.values()):
            self.assertTrue(k in self.dictA)
        for k in list(self.dictA.values()):
            self.assertTrue(k in self.dictB)
            
    def test_DictInvCI_001_03(self):
        """Test '__setitem__' of DictInvCI.""" 
        for i,v in enumerate([9, 8, 'Y', 'Z']):
            self.dictB[list(self.dictB.keys())[i]] = v

        for i,v in enumerate([9, 8, 'Y', 'Z']):
            self.assertTrue(self.dictB[list(self.dictB.keys())[i]] == v)

    def test_DictInvCI_001_04(self):
        """Test '__delitem__' of DictInvCI.""" 
        del self.dictB['FIELD_a']
        del self.dictA['d']
        del self.dictB[1]
        self.assertTrue(len(self.dictA) == len(self.dictB))        


if __name__ == '__main__':
    unittest.main()
