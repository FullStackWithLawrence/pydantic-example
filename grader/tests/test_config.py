# -*- coding: utf-8 -*-
# flake8: noqa: F401
# pylint: disable=duplicate-code
"""
Test integrity of configuration variables.
"""
import pytest  # pylint: disable=unused-import

from ..config import AGRubric, _AGRubric


class TestConfig:
    """Test integrity of configuration variables."""

    def test_configuration_data_types(self):
        """Test the data types of the configuration variables."""
        assert isinstance(
            AGRubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT, float
        ), "INCORRECT_RESPONSE_TYPE_PENALTY_PCT is not a float"
        assert isinstance(
            AGRubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT, float
        ), "INCORRECT_RESPONSE_VALUE_PENALTY_PCT is not a float"
        assert isinstance(AGRubric.RESPONSE_FAILED_PENALTY_PCT, float), "RESPONSE_FAILED_PENALTY_PCT is not a float"
        assert isinstance(
            AGRubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT, float
        ), "INVALID_RESPONSE_STRUCTURE_PENALTY_PCT is not a float"
        assert isinstance(
            AGRubric.INVALID_JSON_RESPONSE_PENALTY_PCT, float
        ), "INVALID_JSON_RESPONSE_PENALTY_PCT is not a float"

    def test_configuration_values(self):
        """Test the values of the configuration variables."""
        assert (
            AGRubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT <= 1.00
        ), "INCORRECT_RESPONSE_TYPE_PENALTY_PCT is greater than 1.00"
        assert (
            AGRubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT >= 0.00
        ), "INCORRECT_RESPONSE_TYPE_PENALTY_PCT is less than 0.00"

        assert (
            AGRubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT <= 1.00
        ), "INCORRECT_RESPONSE_VALUE_PENALTY_PCT is greater than 1.00"
        assert (
            AGRubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT >= 0.00
        ), "INCORRECT_RESPONSE_VALUE_PENALTY_PCT is less than 0.00"

        assert AGRubric.RESPONSE_FAILED_PENALTY_PCT <= 1.00, "RESPONSE_FAILED_PENALTY_PCT is greater than 1.00"
        assert AGRubric.RESPONSE_FAILED_PENALTY_PCT >= 0.00, "RESPONSE_FAILED_PENALTY_PCT is less than 0.00"

        assert (
            AGRubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT <= 1.00
        ), "INVALID_RESPONSE_STRUCTURE_PENALTY_PCT is greater than 1.00"
        assert (
            AGRubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT >= 0.00
        ), "INVALID_RESPONSE_STRUCTURE_PENALTY_PCT is less than 0.00"

        assert (
            AGRubric.INVALID_JSON_RESPONSE_PENALTY_PCT <= 1.00
        ), "INVALID_JSON_RESPONSE_PENALTY_PCT is greater than 1.00"
        assert AGRubric.INVALID_JSON_RESPONSE_PENALTY_PCT >= 0.00, "INVALID_JSON_RESPONSE_PENALTY_PCT is less than 0.00"

    def test_illegal_config_values_low(self):
        """Test illegal configuration values (low)."""
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_TYPE_PENALTY_PCT=-0.01)
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_VALUE_PENALTY_PCT=-0.01)
        with pytest.raises(ValueError):
            _AGRubric(RESPONSE_FAILED_PENALTY_PCT=-0.01)
        with pytest.raises(ValueError):
            _AGRubric(INVALID_RESPONSE_STRUCTURE_PENALTY_PCT=-0.01)
        with pytest.raises(ValueError):
            _AGRubric(INVALID_JSON_RESPONSE_PENALTY_PCT=-0.01)

    def test_illegal_config_values_high(self):
        """Test illegal configuration values (high)."""
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_TYPE_PENALTY_PCT=1.01)
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_VALUE_PENALTY_PCT=1.01)
        with pytest.raises(ValueError):
            _AGRubric(RESPONSE_FAILED_PENALTY_PCT=1.01)
        with pytest.raises(ValueError):
            _AGRubric(INVALID_RESPONSE_STRUCTURE_PENALTY_PCT=1.01)
        with pytest.raises(ValueError):
            _AGRubric(INVALID_JSON_RESPONSE_PENALTY_PCT=1.01)

    def test_illegal_config_values_bad_data_type(self):
        """Test illegal configuration values (bad data type)."""
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_TYPE_PENALTY_PCT="X0.01")
        with pytest.raises(ValueError):
            _AGRubric(INCORRECT_RESPONSE_VALUE_PENALTY_PCT="BAD DATA")
        with pytest.raises(ValueError):
            _AGRubric(RESPONSE_FAILED_PENALTY_PCT="TRUE")
        with pytest.raises(ValueError):
            _AGRubric(INVALID_RESPONSE_STRUCTURE_PENALTY_PCT="_0.01_")
        with pytest.raises(ValueError):
            _AGRubric(INVALID_JSON_RESPONSE_PENALTY_PCT="#0.01")
