# -*- coding: utf-8 -*-
# flake8: noqa: F401
# pylint: disable=duplicate-code
"""
Test integrity of exception classes.
"""
import pytest  # pylint: disable=unused-import

from ..exceptions import (
    VALID_MESSAGE_TYPES,
    AGException,
    IncorrectResponseTypeError,
    IncorrectResponseValueError,
    InvalidJSONResponseError,
    InvalidResponseStructureError,
    ResponseFailedError,
)


class TestExceptions:
    """Test integrity of exception classes."""

    def eval_exception_class(self, exception_class):
        """Evaluate an exception class."""
        try:
            raise exception_class("This is an exception")
        except exception_class as err:
            assert issubclass(
                exception_class, AGException
            ), "IncorrectResponseTypeError is not a subclass of AGException"
            assert err.penalty_pct <= 1.00, "Penalty percentage is greater than 1.00"
            assert err.penalty_pct >= 0.00, "Penalty percentage is less than 0.00"
            assert err.message == "This is an exception", "Incorrect message"
            assert exception_class.__name__ in VALID_MESSAGE_TYPES, "Invalid message type"

    def test_incorrect_response_type(self):
        """Test an incorrect response type."""
        self.eval_exception_class(IncorrectResponseTypeError)

    def test_incorrect_response_value(self):
        """Test an incorrect response value."""
        self.eval_exception_class(IncorrectResponseValueError)

    def test_invalid_json_response(self):
        """Test an invalid JSON response."""
        self.eval_exception_class(InvalidJSONResponseError)

    def test_invalid_response_structure(self):
        """Test an invalid response structure."""
        self.eval_exception_class(InvalidResponseStructureError)

    def test_response_failed(self):
        """Test a failed response."""
        self.eval_exception_class(ResponseFailedError)
