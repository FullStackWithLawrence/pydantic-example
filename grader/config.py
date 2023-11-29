# -*- coding: utf-8 -*-
"""Setup for automated_grader package."""

import os

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, Field


# for local development and unit testing
dotenv_path = find_dotenv()
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, verbose=True)


# pylint: disable=too-few-public-methods
class _AGRubric(BaseModel):
    """Private class to strongly type and bound package configuration params."""

    INCORRECT_RESPONSE_TYPE_PENALTY_PCT: float = Field(0.10, gt=0.00, le=1.00)
    INCORRECT_RESPONSE_VALUE_PENALTY_PCT: float = Field(0.15, gt=0.00, le=1.00)
    RESPONSE_FAILED_PENALTY_PCT: float = Field(0.20, gt=0.00, le=1.00)
    INVALID_RESPONSE_STRUCTURE_PENALTY_PCT: float = Field(0.30, gt=0.00, le=1.00)
    INVALID_JSON_RESPONSE_PENALTY_PCT: float = Field(0.50, gt=0.00, le=1.00)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.INCORRECT_RESPONSE_TYPE_PENALTY_PCT = float(os.getenv("AG_INCORRECT_RESPONSE_TYPE_PENALTY_PCT", "0.10"))
        self.INCORRECT_RESPONSE_VALUE_PENALTY_PCT = float(os.getenv("AG_INCORRECT_RESPONSE_VALUE_PENALTY_PCT", "0.15"))
        self.RESPONSE_FAILED_PENALTY_PCT = float(os.getenv("AG_RESPONSE_FAILED_PENALTY_PCT", "0.20"))
        self.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT = float(
            os.getenv("AG_INVALID_RESPONSE_STRUCTURE_PENALTY_PCT", "0.30")
        )
        self.INVALID_JSON_RESPONSE_PENALTY_PCT = float(os.getenv("AG_INVALID_JSON_RESPONSE_PENALTY_PCT", "0.50"))


ag_rubric = _AGRubric()


class AGRubric:
    """Public class to access package configuration params."""

    INCORRECT_RESPONSE_TYPE_PENALTY_PCT = ag_rubric.INCORRECT_RESPONSE_TYPE_PENALTY_PCT
    INCORRECT_RESPONSE_VALUE_PENALTY_PCT = ag_rubric.INCORRECT_RESPONSE_VALUE_PENALTY_PCT
    RESPONSE_FAILED_PENALTY_PCT = ag_rubric.RESPONSE_FAILED_PENALTY_PCT
    INVALID_RESPONSE_STRUCTURE_PENALTY_PCT = ag_rubric.INVALID_RESPONSE_STRUCTURE_PENALTY_PCT
    INVALID_JSON_RESPONSE_PENALTY_PCT = ag_rubric.INVALID_JSON_RESPONSE_PENALTY_PCT
