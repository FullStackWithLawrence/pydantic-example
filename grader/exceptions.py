# -*- coding: utf-8 -*-
"""Custom exceptions for the AutomatedGrader class."""

from pydantic import BaseModel, Field

from .config import AGRubric


class AGExceptionModel(BaseModel):
    """A Pydantic model for the custom exceptions for the AutomatedGrader class."""

    message: str = Field(..., description="The message to display to the user.")
    penalty_pct: float = Field(
        ..., description="The percentage of the total grade to deduct for this error.", ge=0, le=1
    )


class AGException(Exception):
    """A custom base exception for the AutomatedGrader class."""

    message: str
    penalty_pct: float

    def __init__(self, ag_exception_model: AGExceptionModel):
        super().__init__(ag_exception_model.message)
        self.message = ag_exception_model.message
        self.penalty_pct = ag_exception_model.penalty_pct


class InvalidJSONResponseError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        penalty_pct = AGRubric.INVALID_JSON_RESPONSE_PENALTY_PCT
        ag_exception_model = AGExceptionModel(message=message, penalty_pct=penalty_pct)
        super().__init__(ag_exception_model)


class InvalidResponseStructureError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        penalty_pct = AGRubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT
        ag_exception_model = AGExceptionModel(message=message, penalty_pct=penalty_pct)
        super().__init__(ag_exception_model)


class IncorrectResponseValueError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        penalty_pct = AGRubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT
        ag_exception_model = AGExceptionModel(message=message, penalty_pct=penalty_pct)
        super().__init__(ag_exception_model)


class IncorrectResponseTypeError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        penalty_pct = AGRubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT
        ag_exception_model = AGExceptionModel(message=message, penalty_pct=penalty_pct)
        super().__init__(ag_exception_model)


class ResponseFailedError(AGException):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        penalty_pct = AGRubric.RESPONSE_FAILED_PENALTY_PCT
        ag_exception_model = AGExceptionModel(message=message, penalty_pct=penalty_pct)
        super().__init__(ag_exception_model)


VALID_MESSAGE_TYPES = [
    "Success",
    InvalidJSONResponseError.__name__,
    IncorrectResponseTypeError.__name__,
    IncorrectResponseValueError.__name__,
    InvalidResponseStructureError.__name__,
    ResponseFailedError.__name__,
]
