"""basetestsuite.py
Base class for test suites.
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
from abc import ABC

# Third-Party Packages #
import pytest
from click.testing import CliRunner


# Definitions #
# Fixtures #
@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


# Classes #
class BaseTestSuite(ABC):
    """Base class for test suites."""
