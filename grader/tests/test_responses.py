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

    def test_basic_request(self):
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
