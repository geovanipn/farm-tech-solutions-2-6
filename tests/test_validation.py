from datetime import date
from unittest.mock import patch

from src.utils.validation import read_float, read_int, read_date, read_non_empty


def test_read_float_valid():
    with patch("builtins.input", side_effect=["12.5"]):
        assert read_float("prompt: ") == 12.5


def test_read_float_non_numeric():
    with patch("builtins.input", side_effect=["abc", "12.5"]):
        assert read_float("prompt: ") == 12.5


def test_read_float_out_of_range():
    with patch("builtins.input", side_effect=["150", "80"]):
        assert read_float("prompt: ", max_val=100) == 80.0


def test_read_int_valid():
    with patch("builtins.input", side_effect=["3"]):
        assert read_int("prompt: ") == 3


def test_read_int_non_integer():
    with patch("builtins.input", side_effect=["1.5", "2"]):
        assert read_int("prompt: ") == 2


def test_read_date_valid():
    with patch("builtins.input", side_effect=["25/03/2024"]):
        assert read_date("prompt: ") == date(2024, 3, 25)


def test_read_date_invalid_format():
    with patch("builtins.input", side_effect=["2024-03-25", "25/03/2024"]):
        assert read_date("prompt: ") == date(2024, 3, 25)


def test_read_non_empty_blank():
    with patch("builtins.input", side_effect=["", "  ", "João"]):
        assert read_non_empty("prompt: ") == "João"
