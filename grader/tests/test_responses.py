# -*- coding: utf-8 -*-
# flake8: noqa: F401
# pylint: disable=duplicate-code
"""
Test integrity of automated grader class methods.
"""
import pytest  # pylint: disable=unused-import

from ..grader import AutomatedGrader
from .init import get_event


# pylint: disable=too-few-public-methods
class TestGrader:
    """Test the OpenAI API via Langchain using the Lambda Layer, 'genai'."""

    def test_success(self):
        """Test a valid successful submission."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-correct.json")
        automated_grader = AutomatedGrader(assignment=assignment)
        grade = automated_grader.grade()

        assert isinstance(grade, dict), "The grade is not a dictionary"
        assert "grade" in grade, "The dictionary does not contain the key 'grade'"
        assert isinstance(grade["grade"], int), "The grade is not an int"
        assert grade["grade"] == 100, "The grade is not 100"

        assert "message" in grade, "The dictionary does not contain the key 'message'"
        assert isinstance(grade["message"], str), "The message is not a string"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"

    def test_success_verbose(self):
        """Test a valid successful submission."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-correct-verbose.json")
        automated_grader = AutomatedGrader(assignment=assignment)
        grade = automated_grader.grade()

        assert isinstance(grade, dict), "The grade is not a dictionary"
        assert "grade" in grade, "The dictionary does not contain the key 'grade'"
        assert isinstance(grade["grade"], int), "The grade is not an int"
        assert grade["grade"] == 100, "The grade is not 100"

        assert "message" in grade, "The dictionary does not contain the key 'message'"
        assert isinstance(grade["message"], str), "The message is not a string"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"

    def test_incorrect_response_type(self):
        """Test an assignment with an incorrect response type."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-incorrect-response-type.txt")
        automated_grader = AutomatedGrader(assignment=assignment)
        grade = automated_grader.grade()
        print(grade)

        assert grade["grade"] == 75, "The grade is not 75"
        assert grade["message_type"] == "InvalidResponseStructureError"

    def test_incorrect_response_statuscode(self):
        """Test an assignment with an incorrect response status code."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-incorrect-response-status.json")
        automated_grader = AutomatedGrader(assignment=assignment)

        grade = automated_grader.grade()
        assert grade["message_type"] == "ResponseFailedError"
        assert grade["grade"] == 80, "The grade is not 80"

    def test_incorrect_messages(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-wrong-messages.json")
        automated_grader = AutomatedGrader(assignment=assignment)

        grade = automated_grader.grade()
        assert grade["message_type"] == "IncorrectResponseValueError"
        assert grade["grade"] == 85, "The grade is not 85"

    def test_incorrect_data_type(self):
        """Test an assignment with an incorrect data type."""
        assignment = get_event("tests/events/lawrence-mcdaniel-homework1-type-error.json")
        automated_grader = AutomatedGrader(assignment=assignment)

        grade = automated_grader.grade()
        assert grade["message_type"] == "IncorrectResponseTypeError"
        assert grade["grade"] == 90, "The grade is not 85"
