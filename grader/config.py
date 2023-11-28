# -*- coding: utf-8 -*-
"""Setup for automated_grader package."""

import os

from dotenv import find_dotenv, load_dotenv


# for local development and unit testing
dotenv_path = find_dotenv()
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path, verbose=True)


# pylint: disable=too-few-public-methods
class AGRubric:
    """Constants for the AutomatedGrader class."""

    INCORRECT_RESPONSE_TYPE_PENALTY_PCT = float(os.getenv("AG_INCORRECT_RESPONSE_TYPE_PENALTY_PCT", "0.10"))
    INCORRECT_RESPONSE_VALUE_PENALTY_PCT = float(os.getenv("AG_INCORRECT_RESPONSE_VALUE_PENALTY_PCT", "0.15"))
    RESPONSE_FAILED_PENALTY_PCT = float(os.getenv("AG_RESPONSE_FAILED_PENALTY_PCT", "0.20"))
    INVALID_RESPONSE_STRUCTURE_PENALTY_PCT = float(os.getenv("AG_INVALID_RESPONSE_STRUCTURE_PENALTY_PCT", "0.30"))
