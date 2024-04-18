
from root import MeanReversionBacktest as mbt
from mean_reversion import Defaults
import unittest 
from unittest.mock import patch 


class TestMeanReversionBackest(unittest.TestCase):
    
    # errors 
    def test_validate_integer_input(self):
        
        self.assertRaises(AssertionError, lambda: mbt().validate_integer_input('-1'))
        self.assertRaises(AssertionError, lambda: mbt().validate_integer_input('0',0))
        self.assertTrue(mbt().validate_integer_input(''))
        self.assertTrue(mbt().validate_integer_input('   ')) 
        self.assertFalse(mbt().validate_integer_input('some random string')) 
        self.assertTrue(mbt().validate_integer_input('20',0))
        #self.assertRaises(AssertionError, mbt().validate_integer_input, ['0', 0])
        #self.assertTrue(mbt().validate_integer_input('')) 

    def test_is_blank(self):
        self.assertTrue(mbt().is_blank('   '))
        self.assertFalse(mbt().is_blank('12345'))

    @patch('builtins.input', return_value='')
    def test_get_cash(self, mocked):
        self.assertEqual(mbt().get_cash(), 1000000)