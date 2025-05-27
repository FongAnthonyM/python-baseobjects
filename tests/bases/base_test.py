#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" base_test.py
Common test classes and fixtures for testing base classes in the baseobjects package.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import abc
from pathlib import Path
from typing import Any, Type

# Third-Party Packages #
import pytest


# Definitions #
# Functions #
# Fixtures
@pytest.fixture
def tmp_dir(tmpdir: Any) -> Path:
    """A pytest fixture that turns the tmpdir into a Path object.

    Args:
        tmpdir: A pytest tmpdir fixture.

    Returns:
        Path: A pathlib.Path object representing the temporary directory.
    """
    return Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass.

    This is an abstract base class that defines the interface for all test classes. Subclasses should implement the
    test_instance_creation method and set the class_ attribute.

    Attributes:
        class_: The class that the test class is testing.
    """
    # Attributes #
    class_: Type[Any] | None = None

    # Instance Methods #
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """


# Base Meta
class BaseBaseMetaTest(ClassTest):
    """All BaseMeta subclasses need to pass these tests to considered functional.

    This is an abstract base class that defines the tests that all BaseMeta subclasses should pass. Concrete test
    classes for BaseMeta subclasses should inherit from this class.
    """


# Base Object
class BaseBaseObjectTest(ClassTest):
    """All BaseObject subclasses need to pass these tests to considered functional.

    This is an abstract base class that defines the tests that all BaseObject subclasses should pass. Concrete test
    classes for BaseObject subclasses should inherit from this class.
    """
