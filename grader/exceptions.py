# -*- coding: utf-8 -*-
"""Custom exceptions for the AutomatedGrader class."""


class InvalidResponseStructureError(Exception):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncorrectResponseValueError(Exception):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncorrectResponseTypeError(Exception):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResponseFailedError(Exception):
    """A custom exception for the AutomatedGrader class."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
