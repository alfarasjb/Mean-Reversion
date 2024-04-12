import pytest 
#from ..root import MeanReversionBacktest as mbt
#import mock 
from unittest import mock 
from root import MeanReversionBacktest as mbt
from mean_reversion import Defaults

"""
def test_get_mean_period(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '20')
    assert mbt().get_mean_period() == '20'

def test_get_mean_period_assertion_error(monkeypatch):
    with pytest.raises(AssertionError):
        monkeypatch.setattr('builtins.input', lambda _: '-1')
        mbt().get_mean_period()
"""

#def test_get_mean_period():
#    assert int(mbt().get_mean_period(mean_period='20')) == 20

#def test_get_mean_period_default(): 
#    assert int(mbt().get_mean_period(mean_period='')) == Defaults().mean_period

def test_validate_integer_input_negative_input():
    with pytest.raises(AssertionError):
        mbt().validate_integer_input('-1')

def test_validate_integer_input_minimum_value():
    with pytest.raises(AssertionError):
        mbt().validate_integer_input('0',0)

def test_validate_integer_input_empty_string():
    assert mbt().validate_integer_input('') == True

def test_validate_input_integer_white_spaces():
    assert mbt().validate_integer_input('    ') == True

def test_validate_integer_input_string():
    assert mbt().validate_integer_input('some random string') == False

def test_validate_integer_input_valid():
    assert mbt().validate_integer_input('20',0) == True