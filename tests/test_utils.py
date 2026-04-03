import math
from datetime import date
import pandas as pd
import pytest

from src.compytroller.utils import parse_date, parse_float, parse_int


#  parse_date 
def test_parse_date_valid_formats():
    assert parse_date("2023-05-01") == date(2023, 5, 1)
    assert parse_date("2023-05-01T00:00:00.000") == date(2023, 5, 1)


def test_parse_date_invalid_and_empty():
    assert parse_date(None) is None
    assert parse_date("") is None
    assert parse_date("not-a-date") is None
    assert parse_date(pd.NA) is None  # pandas missing value


#  parse_float 
def test_parse_float_valid_and_with_commas():
    assert parse_float("123.45") == 123.45
    assert parse_float("1,234.56") == 1234.56
    assert parse_float(789) == 789.0


def test_parse_float_invalid_nan_inf():
    assert parse_float(None) is None
    assert parse_float("") is None
    assert parse_float("not-a-float") is None
    assert parse_float("NaN") is None
    assert parse_float(float("nan")) is None
    assert parse_float(float("inf")) is None


#  parse_int 
def test_parse_int_valid_and_with_commas():
    assert parse_int("123") == 123
    assert parse_int("1,234") == 1234
    assert parse_int(567) == 567


def test_parse_int_invalid_nan_inf():
    assert parse_int(None) is None
    assert parse_int("") is None
    assert parse_int("not-an-int") is None
    assert parse_int("NaN") is None
    assert parse_int(float("nan")) is None
    assert parse_int(float("inf")) is None
