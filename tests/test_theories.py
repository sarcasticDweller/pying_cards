from unittest import TestCase
from theories import *

class TestLastMinusFirst(TestCase):
    def setUp(self):
        self.func = last_minus_first_equals_length_minus_one
    
    def test_1_2_3_thusTrue(self):
        seq = [1, 2, 3]
        self.assertTrue(self.func(seq))
    
    def test_4_5_6_thusTrue(self):
        seq = [4, 5, 6]
        self.assertTrue(self.func(seq))
    
    def test_101_102_thusTrue(self):
        seq = [101, 102]
        self.assertTrue(self.func(seq))
    
    def test_1_3_5_thusFalse(self):
        seq = [1, 3, 5]
        self.assertFalse(self.func(seq))

class TestLenAPlusBMinusSumAAlwaysLeBwhensumAleB(TestCase):
    def setUp(self) -> None:
        self.func = lenA_plusB_minus_sumA_always_leB_when_sumA_leB
    
    def test_a_2_3_b_5_thusTrue(self):
        a, b = [2, 3], 5
        expected_value = 2
        _, value = self.func(a, b)
        self.assertEqual(value, expected_value)
    
    def test_a_2_2_b_5_thusTrue(self):
        a, b = [2, 2], 5
        expected_value = 3
        _, value = self.func(a, b)
        self.assertEqual(value, expected_value)
    
    def test_a_2_2_2_b_5_thusTrue(self):
        a, b = [2, 2, 2], 5 
        expected_value = 2
        _, value = self.func(a, b)
        self.assertEqual(value, expected_value)
    
    def test_a_49_347_b_5_thusTrue(self):
        a, b = [49, 347], 5
        r, _ = self.func(a, b)
        self.assertTrue(r)

