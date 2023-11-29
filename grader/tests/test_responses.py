# -*- coding: utf-8 -*-
# flake8: noqa: F401
# pylint: disable=duplicate-code
"""
Test integrity of automated grader class methods.
"""
import pytest  # pylint: disable=unused-import
from pydantic import ValidationError

from ..grader import AutomatedGrader, Grade
from .init import get_event


POTENTIAL_PONTS = 100


# pylint: disable=too-few-public-methods
class TestGrader:
    """Test the OpenAI API via Langchain using the Lambda Layer, 'genai'."""

    def grade(self, assignment_filespec: str, potential_points: int = POTENTIAL_PONTS):
        """Grade an assignment, test its structure and return."""
        assignment = get_event(assignment_filespec)
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=potential_points)
        grade = automated_grader.grade()
        self.grade_structure(grade)
        return grade

    def grade_structure(self, grade):
        """Test the structure of the grade dict."""
        print(grade)
        assert isinstance(grade, dict), "The grade is not a dictionary"
        assert "grade" in grade, "The dictionary does not contain the key 'grade'"
        assert "message" in grade, "The dictionary does not contain the key 'message'"
        assert "message_type" in grade, "The dictionary does not contain the key 'message_type'"
        assert isinstance(grade["grade"], float), "The grade is not an float"
        assert isinstance(grade["message"], str), "The message is not a string"
        assert isinstance(grade["message_type"], str), "The message_type is not a string"
        assert grade["grade"] >= 0, "The grade is less than 0"
        assert grade["grade"] <= POTENTIAL_PONTS, "The grade exceeds the potential points"

    def test_grade_structure(self):
        """Test the structure of the grade dict."""
        g = Grade(grade=100, message="Great job!", message_type="Success")
        self.grade_structure(g.model_dump())

    def test_low_grade(self):
        """Test a low grade."""
        try:
            Grade(grade=-1, message="Great job!", message_type="Success")
        except ValidationError:
            pass
        else:
            raise AssertionError("Grade must be greater than 0")

    def test_grade_invalid_message_type(self):
        """Test an invalid message type."""
        try:
            Grade(grade=-1, message="Great job!", message_type="Not a valid message type")
        except ValidationError:
            pass
        else:
            raise AssertionError("message_type out of range")

    def test_success(self):
        """Test a valid successful submission."""
        grade = self.grade("tests/events/correct.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "Success"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"
        assert grade["grade"] == 100, "The grade is not 100"

    def test_low_potential_points(self):
        """Test a valid successful submission."""
        try:
            self.grade("tests/events/correct.json", potential_points=-1)
        except ValidationError:
            pass
        else:
            raise AssertionError("Potential points must be greater than 0")

    def test_success_verbose(self):
        """Test a valid successful submission."""
        grade = self.grade("tests/events/correct-verbose.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "Success"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"
        assert grade["grade"] == 100, "The grade is not 100"

    def test_bad_data(self):
        """Test an assignment with bad data."""
        grade = self.grade("tests/events/bad-data.txt", potential_points=POTENTIAL_PONTS)

        assert grade["grade"] == 50, "The grade is not 50"
        assert grade["message_type"] == "InvalidJSONResponseError"
        assert grade["message"] == "The assignment is not valid JSON"

    def test_incorrect_response_type(self):
        """Test an assignment with an incorrect response type."""
        grade = self.grade("tests/events/incorrect-response-type.txt", potential_points=POTENTIAL_PONTS)

        assert grade["grade"] == 50, "The grade is not 50"
        assert grade["message_type"] == "InvalidJSONResponseError"
        assert grade["message"] == "The assignment is not valid JSON"

    def test_incorrect_response_statuscode(self):
        """Test an assignment with an incorrect response status code."""
        grade = self.grade("tests/events/incorrect-response-status.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "ResponseFailedError"
        assert grade["grade"] == 80, "The grade is not 80"
        assert grade["message"] == "status_code must be 200. received: 403"

    def test_incorrect_messages(self):
        """Test an assignment with an incorrect message."""
        grade = self.grade("tests/events/wrong-messages.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "The assignment failed pydantic validation."

    def test_incorrect_data_type(self):
        """Test an assignment with an incorrect data type."""
        grade = self.grade("tests/events/type-error.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "The assignment failed pydantic validation."

    def test_bad_message_01(self):
        """Test an assignment with an incorrect message."""
        grade = self.grade("tests/events/bad-message-1.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "The assignment failed pydantic validation."

    def test_bad_message_02(self):
        """Test an assignment with an incorrect message."""
        grade = self.grade("tests/events/bad-message-2.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "messages must contain at least 2 objects"

    def test_bad_message_03(self):
        """Test an assignment with an incorrect message."""
        grade = self.grade("tests/events/bad-message-3.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "The assignment failed pydantic validation."

    def test_bad_message_04(self):
        """Test an assignment with an incorrect message."""
        grade = self.grade("tests/events/bad-message-4.json", potential_points=POTENTIAL_PONTS)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message"] == "The assignment failed pydantic validation."
