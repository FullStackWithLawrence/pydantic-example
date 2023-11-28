# -*- coding: utf-8 -*-
"""Setup for automated_grader package."""
from setuptools import find_packages, setup

from setup_utils import get_semantic_version  # pylint: disable=import-error


setup(
    name="automated_grader",
    version=get_semantic_version(),
    description="Automated grader for Canvas environments",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    packages=find_packages(),
    package_data={
        "automated_grader": ["*.md"],
    },
    install_requires=[],
)
