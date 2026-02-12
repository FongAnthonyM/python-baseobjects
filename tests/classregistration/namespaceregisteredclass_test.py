"""namespaceregisteredclass_test.py
Tests for the NamespaceRegisteredClass class in the baseobjects package.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import NamespaceRegisteredClass
from baseobjects.testsuite.classregistration import NamespaceRegisteredClassTestSuite


# Definitions #
# Classes #
class ConcreteNamespaceRegisteredClass(NamespaceRegisteredClass):
    """A base test subclass of NamespaceRegisteredClass for testing purposes."""

    # Class Attributes #
    class_registration: ClassVar[bool] = True
    class_namespace: ClassVar[str] = "test_namespace"


# Tests #
class TestNamespaceRegisteredClass(NamespaceRegisteredClassTestSuite):
    """Tests the NamespaceRegisteredClass class.

    This class tests the functionality of the NamespaceRegisteredClass class, which is an abstract class that registers
    subclasses with namespaces, allowing subclass dispatching. It creates test subclasses of NamespaceRegisteredClass to
    test with.

    Attributes:
        UnitTestClass: The test class to use for testing, an instance of BaseTestNamespaceRegisteredClass.
    """

    # Attributes #
    UnitTestClass: type[ConcreteNamespaceRegisteredClass] = ConcreteNamespaceRegisteredClass

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected", "error"),
        [
            (("any", "any"), {"default": "default"}, "default", None),
            (("any", "any"), {}, None, KeyError),
        ],
    )
    def test_get_registered_class_no_registry(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected: Any,
        error: type[Exception] | None,
    ) -> None:
        """Tests get_registered_class when no registry is present."""
        if error:
            with pytest.raises(error):
                NamespaceRegisteredClass.get_registered_class(*args, **kwargs)
        else:
            result = NamespaceRegisteredClass.get_registered_class(*args, **kwargs)
            assert result == expected


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
