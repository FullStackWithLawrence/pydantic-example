# -*- coding: utf-8 -*-
"""Custom exceptions for the AutomatedGrader class."""

from .config import AGRubric


class AGException(Exception):
    """A custom base exception for the AutomatedGrader class."""

    def __init__(self, message: str, penalty_pct: float):
        self.message = message

        if not isinstance(penalty_pct, float):
            raise TypeError(f"penalty_pct must be a float. penalty_pct: {penalty_pct}")
        if not 0 <= penalty_pct <= 1:
            raise ValueError(f"penalty_pct must be between 0 and 1. penalty_pct: {penalty_pct}")

        self._penalty_pct = penalty_pct
        super().__init__(self.message)

    @property
    def penalty_pct(self):
        """Return the penalty percentage for this error."""
        return self._penalty_pct


class InvalidResponseStructureError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message, penalty_pct=AGRubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT)


class IncorrectResponseValueError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message, penalty_pct=AGRubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT)


class IncorrectResponseTypeError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message, penalty_pct=AGRubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT)


class ResponseFailedError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message, penalty_pct=AGRubric.RESPONSE_FAILED_PENALTY_PCT)
