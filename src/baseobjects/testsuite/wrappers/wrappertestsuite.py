"""wrappertestsuite.py
Specialized test suite for wrapper classes.

This module contains the specialized test suite for wrapper classes.
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
    """Tests suite for wrapper classes.

    This class provides concrete implementations of the abstract methods defined in BaseWrapperTestSuite.
    It includes example classes for testing wrapper functionality.

    Attributes:
        UnitTestClass: The wrapper class that the test suite is testing.
    """

    class ConcreteOne:
        """An example class for testing wrappers.

        This class has attributes and methods that can be wrapped by wrapper classes.
        """

        # Attributes #
        one: str
        two: str = "one"
        common: str = "example_one"

        def __init__(self) -> None:
            """Initializes with attributes."""
            self.one = "one"
            self.two = "one"
            self.common = "example_one"

        def __eq__(self, other: Any) -> bool:
            """Checks equality with another object.

            Args:
                other: The object to compare with.

            Returns:
                Always True.
            """
            return True

        def method(self) -> str:
            """Returns a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "one"

        def __str__(self) -> str:
            """Returns a string representation of this class."""
            return "ConcreteOne"

    class ConcreteTwo:
        """Another example class for testing wrappers.

        This class has different attributes and methods than ConcreteOne.
        """

        # Attributes #
        one: str
        three: str
        common: str

        def __init__(self) -> None:
            """Initializes with attributes."""
            self.one = "two"
            self.three = "two"
            self.common = "example_two"

        def function(self) -> str:
            """Returns a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "two"

        def __str__(self) -> str:
            """Returns a string representation of this class."""
            return "ConcreteTwo"

    # Fixtures #
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> Any:
        """Creates a new test object.

        This method creates a new instance of the UnitTestClass with ConcreteOne and ConcreteTwo objects.

        Returns:
            A new test object.
        """
        return self.UnitTestClass(self.ConcreteOne(), self.ConcreteTwo())

    # Tests #
    # Instantiation #
    @pytest.mark.parametrize("arg_count", [0, 1, 2])
    def test_instance_creation(self, arg_count: int, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the wrapper class can be created.

        This test verifies that instances of the UnitTestClass can be created with various arguments.

        Args:
            arg_count: The number of arguments to use for creation.
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if arg_count == 0:
            creation_args = []
        elif arg_count == 1:
            creation_args = [self.ConcreteOne()]
        else:
            creation_args = [self.ConcreteOne(), self.ConcreteTwo()]  # type: ignore[list-item]

        instance = self.UnitTestClass(*creation_args)
        assert isinstance(instance, self.UnitTestClass)

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_wrapper_copy(self, test_object: Any, method: str) -> None:
        """Tests copying a wrapper object.

        This test verifies that wrapper objects can be copied correctly, and that the copy shares the same wrapped
        objects.

        Args:
            test_object: The test object to copy.
            method: The method used to copy the object.

        Raises:
            ValueError: If the method is invalid.
        """
        # Copy Object
        if method == "copy":
            wrapper = copy.copy(test_object)
        elif method == "method":
            wrapper = test_object.copy()
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert id(wrapper._first) == id(test_object._first)
        assert id(wrapper._second) == id(test_object._second)

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_wrapper_deepcopy(self, test_object: Any, method: str, memo: dict[Any, Any] | None = None) -> None:
        """Tests deep copying a wrapper object.

        This test verifies that wrapper objects can be deep copied correctly, and that the deep copy has different
        wrapped objects.

        Args:
            test_object: The test object to deep copy.
            method: The method used to deep copy the object.
            memo: A memo dictionary to pass to deepcopy.

        Raises:
            ValueError: If the method is invalid.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            wrapper = copy.deepcopy(test_object, memo=memo)
        elif method == "method":
            wrapper = test_object.deepcopy(memo=memo)
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert id(wrapper._first) != id(test_object._first)
        assert id(wrapper._second) != id(test_object._second)

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of a wrapper object.

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

    # Functionality #
    def test_wrapper_overrides(self) -> None:
        """Tests that wrapper attributes and methods override wrapped objects.

        This test verifies that attributes and methods defined in the wrapper take precedence over those in wrapped
        objects.
        """
        # Sets attributes and methods on the wrapper
        test_wrapper = self.UnitTestClass(self.ConcreteOne(), self.ConcreteTwo())
        test_wrapper.two = "wrapper"  # type: ignore[attr-defined]
        test_wrapper.four = "wrapper"  # type: ignore[attr-defined]
        test_wrapper.wrap = lambda: "wrapper"  # type: ignore[attr-defined]

        # Verifies that wrapper attributes and methods override wrapped objects
        assert test_wrapper.two == "wrapper"  # type: ignore[attr-defined]
        assert test_wrapper.four == "wrapper"  # type: ignore[attr-defined]
        assert test_wrapper.wrap() == "wrapper"  # type: ignore[attr-defined]

    @pytest.mark.parametrize("action", ["set", "del"])
    def test_attribute_modification(self, action: str) -> None:
        """Tests setting and deleting attributes on wrapped objects.

        This test verifies that setting/deleting attributes through the wrapper correctly updates the wrapped objects.

        Args:
            action: The action to perform ('set' or 'del').
        """
        test_wrapper = self.UnitTestClass(self.ConcreteOne(), self.ConcreteTwo())

        if action == "set":
            test_wrapper.one = "set"  # type: ignore[attr-defined]
            assert test_wrapper._first.one == "set"  # type: ignore[attr-defined]
        elif action == "del":
            del test_wrapper.one  # type: ignore[attr-defined]
            assert "one" not in dir(test_wrapper._first)  # type: ignore[attr-defined]

    @pytest.mark.xfail
    def test_magic_inheritance(self, test_object: Any) -> None:
        """Tests that magic methods are inherited from wrapped objects. (They are not currently).

        This test verifies that magic methods from wrapped objects are accessible through the wrapper. The equality
        magic method is being tested here. This test is expected to fail.

        Args:
            test_object: The test object to check.
        """
        assert test_object == 1

    def test_conflicting_attributes(self, test_object: Any) -> None:
        """Tests how the wrapper handles attributes with the same name in multiple wrapped objects.

        This test verifies that when multiple wrapped objects have attributes with the same name, the attribute from the
        first wrapped object in the resolution order is used.

        Args:
            test_object: The test object to check.
        """
        assert test_object.common == "example_one"

    def test_none_wrapped_object(self) -> None:
        """Tests how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects without raising exceptions during
        normal operations.
        """
        # Creates a wrapper with None as the wrapped object
        wrapper = self.UnitTestClass(None)

        # Verifies that accessing attributes doesn't raise exceptions
        assert wrapper._first is None  # type: ignore[attr-defined]

        # Verifies that accessing non-existent attributes raises AttributeError
        with pytest.raises(AttributeError):
            _ = wrapper.non_existent_attribute  # type: ignore[attr-defined]

    def test_nested_wrappers(self) -> None:
        """Tests how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper, and that attribute
        access works correctly through multiple levels of wrapping.
        """
        # Creates a wrapper
        wrapper1 = self.UnitTestClass(self.ConcreteOne())

        # Creates a wrapper that wraps the first wrapper
        wrapper2 = self.UnitTestClass(wrapper1)

        # Verifies that attribute access works through multiple levels of wrapping
        assert wrapper2.one == "one"  # type: ignore[attr-defined]
        assert wrapper2.method() == "one"  # type: ignore[attr-defined]

        # Verifies that setting attributes works through multiple levels of wrapping
        wrapper2.one = "nested"  # type: ignore[attr-defined]
        assert wrapper1.one == "nested"  # type: ignore[attr-defined]
        assert wrapper1._first.one == "nested"  # type: ignore[attr-defined]
