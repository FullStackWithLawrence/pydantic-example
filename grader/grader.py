# -*- coding: utf-8 -*-
"""Provide a class for grading a submission against an assignment.""" ""

import json

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from .exceptions import (
    VALID_MESSAGE_TYPES,
    AGException,
    IncorrectResponseTypeError,
    IncorrectResponseValueError,
    InvalidResponseStructureError,
    ResponseFailedError,
)
from .langchain import LCResponse


class Grade(BaseModel):
    """
    This is the base class for all Grader types. It provides the common interface and
    functionality for grading, but does not implement the grading logic itself.
    Subclasses should override the necessary methods to provide the grading logic.
    """

    potential_points: float = Field(100, description="The maximum number of points that can be awarded.", ge=0)
    grade: float = Field(..., description="The number of points awarded.", ge=0)
    message: str = Field(..., description="A result message to the student.")
    message_type: str = Field(..., description="The type of result message.")

    @model_validator(mode="after")
    def validate_grade(self) -> "Grade":
        """Validate that the grade is >= 0 and <= potential_points"""
        if self.grade < 0:
            raise ValueError(f"grade must be at least 0.00. received: {self.grade}")
        if self.grade > self.potential_points:
            raise ValueError(f"grade must be less than or equal to potential_points. received: {self.grade}")
        return self

    @field_validator("message_type")
    @classmethod
    def message_type_is_valid(cls, message_type):
        """Validate that the message_type is valid"""
        if message_type not in VALID_MESSAGE_TYPES:
            raise ValueError(f"message_type must be one of {VALID_MESSAGE_TYPES}")
        return message_type


# flake8: noqa: E701
class AutomatedGrader(BaseModel):
    """Grade a submission against an assignment."""

    assignment: str = Field(..., description="The assignment to grade.")
    potential_points: float = Field(100, description="The maximum number of points that can be awarded.", ge=0)

    def grade_response(self, message: AGException = None):
        """Create a grade dict from the assignment."""
        grade = self.potential_points * (1 - (message.penalty_pct if message else 0))
        message_type = message.__class__.__name__ if message else "Success"
        message = str(message) if message else "Great job!"

        grade = Grade(grade=grade, message=message, message_type=message_type, potential_points=self.potential_points)
        return grade.model_dump()

    def grade(self):
        """Grade the assignment."""
        assignment_json: dict
        lc_response: LCResponse

        # 1.) attempt to load the assignment as JSON
        try:
            assignment_json = json.loads(self.assignment)
        except json.JSONDecodeError as e:
            try:
                raise InvalidResponseStructureError("The assignment is not valid JSON") from e
            except InvalidResponseStructureError as reraised_e:
                return self.grade_response(reraised_e)

        # 2.) attempt to validate the assignment using Pydantic
        try:
            lc_response = LCResponse(**assignment_json)
        except (ValidationError, TypeError) as e:
            try:
                raise InvalidResponseStructureError("The assignment failed pydantic validation.") from e
            except InvalidResponseStructureError as reraised_e:
                return self.grade_response(reraised_e)

        # 3.) validate the assignment
        try:
            lc_response.validate_response()
            return self.grade_response()
        except (
            ResponseFailedError,
            InvalidResponseStructureError,
            ResponseFailedError,
            IncorrectResponseValueError,
            IncorrectResponseTypeError,
        ) as e:
            return self.grade_response(e)
