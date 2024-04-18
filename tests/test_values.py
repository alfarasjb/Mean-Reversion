
from root import MeanReversionBacktest
import mean_reversion
import unittest 
from unittest.mock import patch 



class TestMeanReversionBackestValues(unittest.TestCase):
    
    def setUp(self):
        self.mbt = MeanReversionBacktest()
        self.defaults = mean_reversion.Defaults()
        self.rolling_calc = mean_reversion.RollingCalculationType()
        self.side = mean_reversion.Side()
        self.default_mean_period = self.defaults.mean_period 
        self.default_spread_mean_period = self.defaults.spread_mean_period
        self.default_spread_sdev_period = self.defaults.spread_sdev_period
        self.default_threshold = self.defaults.threshold
        self.default_calculation_type = self.defaults.calc_type
        self.default_side = self.defaults.side 
        
    
    # ----------------------------- testing defaults ----------------------------- #

    @patch('builtins.input', return_value='')    
    def test_get_mean_period(self, mocked):
        self.assertEqual(self.mbt.get_mean_period(), self.default_mean_period)

    @patch('builtins.input', return_value='')
    def test_get_spread_mean_period(self, mocked):
        self.assertEqual(self.mbt.get_spread_mean_period(), self.default_spread_mean_period)

    @patch('builtins.input', return_value='')
    def test_get_spread_sdev_period(self, mocked): 
        self.assertEqual(self.mbt.get_spread_sdev_period(), self.default_spread_sdev_period)

    @patch('builtins.input', return_value = '')
    def test_get_threshold(self, mocked):
        self.assertEqual(self.mbt.get_threshold(), self.default_threshold)

    @patch('builtins.input', return_value = '')
    def test_get_calculation_type(self, mocked):
        self.assertEqual(self.mbt.get_calculation_type(), self.default_calculation_type)

    @patch('builtins.input', return_value='')
    def test_get_side(self, mocked):
        self.assertEqual(self.mbt.get_side(), self.default_side)

    
    # ----------------------------- testing values ----------------------------- #
    @patch('builtins.input', return_value = '1')
    def test_get_calculation_type_valid_int(self, mocked):
        calc = self.rolling_calc.valid_values[int(mocked())-1]
        self.assertEqual(self.mbt.get_calculation_type(), calc)

    @patch('builtins.input', return_value='Simple')
    def test_get_calculation_type_str(self, mocked):
        calc = self.rolling_calc.calculation_simple
        self.assertEqual(self.mbt.get_calculation_type(), calc)

    @patch('builtins.input', return_value='1')
    def test_get_side_valid_int(self, mocked):
        side = self.side.valid_values[int(mocked())-1]
        self.assertEqual(self.mbt.get_side(), side)

    @patch('builtins.input', return_value='Long')
    def test_get_side_valid_str(self, mocked):
        side = self.side.side_long 
        self.assertEqual(self.mbt.get_side(), side)
