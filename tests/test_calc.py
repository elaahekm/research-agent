import pytest

from calc_tool import calculate


def test_multiply():
    assert calculate("12 * (3 + 4)") == 84


def test_percent_as_decimal():
    assert calculate("0.15 * 2400") == 360


def test_rejects_unsafe_code():
    with pytest.raises(ValueError):
        calculate("__import__('os')")