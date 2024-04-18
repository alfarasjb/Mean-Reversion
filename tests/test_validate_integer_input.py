
from root import MeanReversionBacktest
from mean_reversion import Defaults, Accounts
import unittest 
from unittest.mock import patch 


class TestIntegerInput(unittest.TestCase):
    
    
    def setUp(self):
        self.mbt = MeanReversionBacktest()

    # errors 
    def test_validate_integer_input(self):
        self.assertRaises(AssertionError, lambda: self.mbt.validate_integer_input('-1'))
        self.assertRaises(AssertionError, lambda: self.mbt.validate_integer_input('0',0))
        self.assertTrue(self.mbt.validate_integer_input(''))
        self.assertTrue(self.mbt.validate_integer_input('   ')) 
        self.assertFalse(self.mbt.validate_integer_input('some random string')) 
        self.assertTrue(self.mbt.validate_integer_input('20',0))
        

    def test_is_blank(self):
        self.mbt = MeanReversionBacktest()
        self.assertTrue(self.mbt.is_blank('   '))
        self.assertFalse(self.mbt.is_blank('12345'))

