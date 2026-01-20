#!/usr/bin/env python
"""parameters_test.py
Test for the Parameters class.
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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.dataclasses import Parameters


# Definitions #
# Classes #
class TestParameters:
    """Tests the Parameters class.

    This class tests the functionality of the Parameters class.
    """

    # Attributes #
    UnitTestClass = Parameters

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("init_args", "init_kwargs", "expected_args", "expected_kwargs"),
        [
            ([], {}, (), {}),
            ([], {"args": (1, 2), "kwargs": {"a": 3}}, (1, 2), {"a": 3}),
            ([(1, 2), {"a": 3}], {}, (1, 2), {"a": 3}),
        ],
    )
    def test_init(
        self,
        init_args: list[Any],
        init_kwargs: dict[str, Any],
        expected_args: tuple[Any, ...],
        expected_kwargs: dict[str, Any],
    ) -> None:
        """Tests initialization with various arguments."""
        params = self.UnitTestClass(*init_args, **init_kwargs)
        assert params.args == expected_args
        assert params.kwargs == expected_kwargs

    @pytest.mark.parametrize(
        ("args", "kwargs"),
        [
            ((), {}),
            ((1, 2), {"a": 3}),
        ],
    )
    def test_unpacking(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
        """Tests unpacking."""
        params = self.UnitTestClass(args, kwargs)
        unpacked_args, unpacked_kwargs = params
        assert unpacked_args == args
        assert unpacked_kwargs == kwargs


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
