import pytest 
from unittest import mock 
from root import MeanReversionBacktest as mbt
from mean_reversion import Defaults, RollingCalculationType, Side
""" 
def test_get_mean_period(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_mean_period() == '20'
""" 

"""
#def test_get_spread_mean_period(monkeypatch):
#    monkeypatch.setattr('builtins.input', lambda _: '20')
#    assert mbt().get_spread_mean_period() == 20

def test_get_mean_period_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_mean_period() == Defaults().mean_period

def test_get_spread_mean_period_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_spread_mean_period() == Defaults().spread_mean_period

def test_get_spread_sdev_period_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_spread_sdev_period() == Defaults().spread_sdev_period

def test_get_threshold_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_threshold() == Defaults().threshold

def test_get_calculation_type(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_calculation_type() == Defaults().calc_type 

def test_get_side(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert mbt().get_side() == Defaults().side

def test_get_mean_period_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_mean_period() == 20 

def test_get_spread_mean_period_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_spread_mean_period() == 20 

def test_get_spread_sdev_period_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_spread_sdev_period() == 20 

def test_get_threshold_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_threshold() == 20 

def test_get_calculation_type_valid_int(monkeypatch):
    input_value = '1'
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    assert mbt().get_calculation_type() == RollingCalculationType().valid_values[int(input_value)-1]

def test_get_calculation_type_valid_str(monkeypatch):
    input_value='Simple'
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    assert mbt().get_calculation_type() == RollingCalculationType().calculation_simple 

def test_get_side_valid_int(monkeypatch):
    input_value = '1'
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    assert mbt().get_side() == Side().side_long 

def test_get_side_valid_str(monkeypatch):
    input_value = 'Long'
    monkeypatch.setattr('builtins.input', lambda _: input_value)
    assert mbt().get_side() == Side().side_long

    """