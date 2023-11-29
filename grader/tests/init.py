# -*- coding: utf-8 -*-
"""Provide common functions for testing."""


def get_event(filespec):
    """Reads a JSON file and returns the event"""
    with open(filespec, "r", encoding="utf-8") as f:  # pylint: disable=invalid-name
        return f.read()
