# -*- coding: utf-8 -*-
# flake8: noqa: F401
# pylint: disable=duplicate-code
"""
Test integrity of automated grader class methods.
"""
import pytest  # pylint: disable=unused-import

from ..grader import AutomatedGrader
from .init import get_event


POTENTIAL_PONTS = 100


# pylint: disable=too-few-public-methods
class TestGrader:
    """Test the OpenAI API via Langchain using the Lambda Layer, 'genai'."""

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

    def test_success(self):
        """Test a valid successful submission."""
        assignment = get_event("tests/events/correct.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "Success"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"
        assert grade["grade"] == 100, "The grade is not 100"

    def test_success_verbose(self):
        """Test a valid successful submission."""
        assignment = get_event("tests/events/correct-verbose.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "Success"
        assert grade["message"] == "Great job!", "The message is not 'Great job!'"
        assert grade["grade"] == 100, "The grade is not 100"

    def test_bad_data(self):
        """Test an assignment with bad data."""
        assignment = get_event("tests/events/bad-data.txt")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message_type"] == "InvalidResponseStructureError"

    def test_incorrect_response_type(self):
        """Test an assignment with an incorrect response type."""
        assignment = get_event("tests/events/incorrect-response-type.txt")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["grade"] == 70, "The grade is not 70"
        assert grade["message_type"] == "InvalidResponseStructureError"

    def test_incorrect_response_statuscode(self):
        """Test an assignment with an incorrect response status code."""
        assignment = get_event("tests/events/incorrect-response-status.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "ResponseFailedError"
        assert grade["grade"] == 80, "The grade is not 80"

    def test_incorrect_messages(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/wrong-messages.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"

    def test_incorrect_data_type(self):
        """Test an assignment with an incorrect data type."""
        assignment = get_event("tests/events/type-error.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"

    def test_bad_message_01(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/bad-message-1.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"

    def test_bad_message_02(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/bad-message-2.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"

    def test_bad_message_03(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/bad-message-3.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"

    def test_bad_message_04(self):
        """Test an assignment with an incorrect message."""
        assignment = get_event("tests/events/bad-message-4.json")
        automated_grader = AutomatedGrader(assignment=assignment, potential_points=POTENTIAL_PONTS)
        grade = automated_grader.grade()
        self.grade_structure(grade)

        assert grade["message_type"] == "InvalidResponseStructureError"
        assert grade["grade"] == 70, "The grade is not 70"
