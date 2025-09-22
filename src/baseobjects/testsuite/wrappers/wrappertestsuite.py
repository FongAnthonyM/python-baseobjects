"""wrappertestsuite.py
Specialized test suite for wrapper classes.
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
import copy
import pickle
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class WrapperTestSuite(BaseObjectTestSuite):
    """Test suite for wrapper classes.

    This class provides concrete implementations of the abstract methods defined in BaseWrapperTestSuite.
    It includes example classes for testing wrapper functionality.

    Attributes:
        TestClass: The wrapper class that the test suite is testing.
    """

    # Class Definitions #
    class ExampleOne:
        """An example class for testing wrappers.

        This class has attributes and methods that can be wrapped by wrapper classes.
        """

        # Attributes #
        one: str
        two: str = "one"
        common: str = "example_one"

        def __init__(self) -> None:
            """Initialize with attributes."""
            self.one = "one"
            self.two = "one"
            self.common = "example_one"

        def __eq__(self, other: Any) -> bool:
            """Always return True for equality comparison."""
            return True

        def method(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "one"

        def __str__(self) -> str:
            """Return a string representation of this class."""
            return "ExampleOne"

    class ExampleTwo:
        """Another example class for testing wrappers.

        This class has different attributes and methods than ExampleOne.
        """

        # Attributes #
        one: str
        three: str
        common: str

        def __init__(self) -> None:
            """Initialize with attributes."""
            self.one = "two"
            self.three = "two"
            self.common = "example_two"

        def function(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "two"

        def __str__(self) -> str:
            """Return a string representation of this class."""
            return "ExampleTwo"

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> Any:
        """Create a new test object.

        This method creates a new instance of the TestClass with ExampleOne and ExampleTwo objects.

        Returns:
            A new test object.
        """
        return self.TestClass(self.ExampleOne(), self.ExampleTwo())

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the wrapper class can be created.

        This test verifies that instances of the TestClass can be created with various arguments.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Test with no arguments
        instance = self.TestClass()
        assert isinstance(instance, self.TestClass)

        # Test with one argument
        instance = self.TestClass(self.ExampleOne())
        assert isinstance(instance, self.TestClass)

        # Test with multiple arguments
        instance = self.TestClass(self.ExampleOne(), self.ExampleTwo())
        assert isinstance(instance, self.TestClass)

    def test_copy(self, test_object: Any) -> None:
        """Test copying a wrapper object.

        This test verifies that wrapper objects can be copied correctly, and that the copy shares the same wrapped
        objects.

        Args:
            test_object: The test object to copy.
        """
        # Copy Object
        wrapper = copy.copy(test_object)

        # Validate
        assert id(wrapper._first) == id(test_object._first)
        assert id(wrapper._second) == id(test_object._second)

    def test_copy_method(self, test_object: Any) -> None:
        """Test copying a wrapper object with its own copy method.

        This test verifies that wrapper objects can be copied correctly, and that the copy shares the same wrapped
        objects.

        Args:
            test_object: The test object to copy.
        """
        # Copy Object
        wrapper = test_object.copy()

        # Validate
        assert id(wrapper._first) == id(test_object._first)
        assert id(wrapper._second) == id(test_object._second)

    def test_deepcopy(self, test_object: Any, memo: dict | None = None) -> None:
        """Test deep copying a wrapper object.

        This test verifies that wrapper objects can be deep copied correctly, and that the deep copy has different
        wrapped objects.

        Args:
            test_object: The test object to deep copy.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        wrapper = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert id(wrapper._first) != id(test_object._first)
        assert id(wrapper._second) != id(test_object._second)

    def test_deepcopy_method(self, test_object: Any, memo: dict | None = None) -> None:
        """Test deep copying a wrapper object with its own deep copy method.

        This test verifies that wrapper objects can be deep copied correctly, and that the deep copy has different
        wrapped objects.

        Args:
            test_object: The test object to deep copy.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        wrapper = test_object.deepcopy()

        # Validate
        assert id(wrapper._first) != id(test_object._first)
        assert id(wrapper._second) != id(test_object._second)

    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of a wrapper object.

        This test verifies that wrapper objects can be pickled and unpickled correctly.

        Args:
            test_object: The test object to pickle and unpickle.
        """
        # Pickle and Unpickle Object
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)

        # Validate
        assert new_obj is not test_object
        assert new_obj._first is not test_object._first
        assert set(dir(new_obj)) == set(dir(test_object))

    def test_wrapper_overrides(self) -> None:
        """Test that wrapper attributes and methods override wrapped objects.

        This test verifies that attributes and methods defined in the wrapper take precedence over those in wrapped
        objects.
        """
        # Set attributes and methods on the wrapper
        test_wrapper = self.TestClass(self.ExampleOne(), self.ExampleTwo())
        test_wrapper.two = "wrapper"
        test_wrapper.four = "wrapper"
        test_wrapper.wrap = lambda: "wrapper"

        # Verify that wrapper attributes and methods override wrapped objects
        assert test_wrapper.two == "wrapper"
        assert test_wrapper.four == "wrapper"
        assert test_wrapper.wrap() == "wrapper"

    def test_setting_wrapped(self) -> None:
        """Test setting attributes on wrapped objects.

        This test verifies that setting attributes through the wrapper correctly updates the wrapped objects.
        """
        test_wrapper = self.TestClass(self.ExampleOne(), self.ExampleTwo())
        test_wrapper.one = "set"
        assert test_wrapper._first.one == "set"

    def test_deleting_wrapped(self) -> None:
        """Test deleting attributes on wrapped objects.

        This test verifies that deleting attributes through the wrapper correctly removes them from the wrapped objects.
        """
        test_wrapper = self.TestClass(self.ExampleOne(), self.ExampleTwo())
        del test_wrapper.one
        assert "one" not in dir(test_wrapper._first)

    @pytest.mark.xfail
    def test_magic_inheritance(self, test_object: Any) -> None:
        """Test that magic methods are inherited from wrapped objects. (They are not currently)

        This test verifies that magic methods from wrapped objects are accessible through the wrapper. The equality
        magic method is being tested here. This test is expected to fail.

        Args:
            test_object: The test object to check.
        """
        assert test_object == 1

    def test_conflicting_attributes(self, test_object: Any) -> None:
        """Test how the wrapper handles attributes with the same name in multiple wrapped objects.

        This test verifies that when multiple wrapped objects have attributes with the same name, the attribute from the
        first wrapped object in the resolution order is used.

        Args:
            test_object: The test object to check.
        """
        assert test_object.common == "example_one"

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects without raising exceptions during
        normal operations.
        """
        # Create a wrapper with None as the wrapped object
        wrapper = self.TestClass(None)

        # Verify that accessing attributes doesn't raise exceptions
        assert wrapper._first is None

        # Verify that accessing non-existent attributes raises AttributeError
        with pytest.raises(AttributeError):
            wrapper.non_existent_attribute

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper, and that attribute
        access works correctly through multiple levels of wrapping.
        """
        # Create a wrapper
        wrapper1 = self.TestClass(self.ExampleOne())

        # Create a wrapper that wraps the first wrapper
        wrapper2 = self.TestClass(wrapper1)

        # Verify that attribute access works through multiple levels of wrapping
        assert wrapper2.one == "one"
        assert wrapper2.method() == "one"

        # Verify that setting attributes works through multiple levels of wrapping
        wrapper2.one = "nested"
        assert wrapper1.one == "nested"
        assert wrapper1._first.one == "nested"
