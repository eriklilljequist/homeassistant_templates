from unittest.mock import MagicMock
from src.utilities import utils


def test__as_float__happy():
    value = utils.as_float(logger=MagicMock(), string='0.1', or_else=0.2, not_less_than=0)
    assert value == 0.1


def test__as_float__not_less_than():
    value = utils.as_float(logger=MagicMock(), string='0.1', or_else=0.2, not_less_than=1)
    assert value == 1


def test__as_float__non_float_string():
    value = utils.as_float(logger=MagicMock(), string='foobar', or_else=0.2, not_less_than=1)
    assert value == 1


def test__as_float__default_not_less_then():
    value = utils.as_float(logger=MagicMock(), string='foobar', or_else=0.2)
    assert value == 0.2


def test__as_float__default_not_less_then__():
    value = utils.as_float(logger=MagicMock(), string='None', or_else=0.2)
    assert value == 0.2
