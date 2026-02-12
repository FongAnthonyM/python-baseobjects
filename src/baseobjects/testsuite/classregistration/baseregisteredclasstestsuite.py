"""baseregisteredclasstestsuite.py
Base test suite for BaseRegisteredClass and its subclasses.
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
from ...classregistration import BaseClassRegistry, BaseRegisteredClass
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class MockRegistry(BaseClassRegistry):
    """A mock registry for testing."""

    def __init__(self, head_class: type | None = None, init: bool = True, **kwargs: Any) -> None:
        """Initializes the MockRegistry."""
        self.registered: list[type] = []
        super().__init__(head_class=head_class, init=init, **kwargs)

    def register_class(self, cls: type, *args: Any, **kwargs: Any) -> None:
        """Registers a class."""
        self.registered.append(cls)

    def get_class(self, *args: Any, **kwargs: Any) -> Any:
        """Gets a class.

        Returns:
            Always returns None.
        """
        return None


class BaseRegisteredClassTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseRegisteredClass.

    This class provides common test functionality for child classes of BaseRegisteredClass, including tests for class
    registration and retrieval. Subclasses should set the UnitTestClass attribute and may override or extend the test
    methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: type[BaseRegisteredClass]

    # Fixtures #
    @pytest.fixture
    def example_subclass(self) -> type[BaseRegisteredClass]:
        """Creates a test subclass of the UnitTestClass.

        Returns:
            A test subclass of the UnitTestClass.
        """

        class TestSubclass(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registration = True

        return TestSubclass

    # Tests #
    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: Any, method: str) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method of copying to test.

        Raises:
            ValueError: If the method is invalid.
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        elif method == "method":
            obj_copy = test_object.copy()
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(self, test_object: Any, method: str, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method of deepcopying to test.
            memo: A memo dictionary to pass to deepcopy.

        Raises:
            ValueError: If the method is invalid.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        elif method == "method":
            obj_deepcopy = test_object.deepcopy(memo=memo)
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)

    # Functionality #
    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Tests the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to the register_class method.
            **kwargs: Keyword arguments to pass to the register_class method.
        """

        class NewTestSubclass(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registration = False

        # Register class
        NewTestSubclass.register_class(*args, **kwargs)

        # Verify class was registered
        assert self.UnitTestClass.class_registry is not None
        assert NewTestSubclass.__name__ in self.UnitTestClass.class_registry
        assert self.UnitTestClass.class_registry[NewTestSubclass.__name__] is NewTestSubclass

    def test_get_registered_class(self, example_subclass: type[BaseRegisteredClass], *args: Any, **kwargs: Any) -> None:
        """Tests the get_registered_class method.

        This test verifies that the get_registered_class method correctly retrieves a registered class.

        Args:
            example_subclass: A fixture providing a test subclass.
            *args: Positional arguments to test the get_register_class method.
            **kwargs: Keyword arguments to test the get_register_class method.
        """
        # Register class
        got_class = self.UnitTestClass.get_registered_class(example_subclass.__name__)

        # Verify class was registered
        assert self.UnitTestClass.class_registry is not None
        assert example_subclass.__name__ in self.UnitTestClass.class_registry
        assert got_class is example_subclass

    def test_head_class_assignment(self) -> None:
        """Tests that head_class is assigned to the registry if it's missing."""
        registry = MockRegistry(head_class=None)

        class Base(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registry_type = MockRegistry
            class_registry = None
            class_registration = False  # Don't trigger auto-creation

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> Any:
                return None

        Base.class_registry = registry  # type: ignore[assignment]

        class Child(Base):
            class_registration = True

        assert registry.head_class == Child
        assert Child in registry.registered

    def test_register_class_default(self) -> None:
        """Tests the default register_class implementation."""

        class DefaultRegClass(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registry_type = MockRegistry
            class_registry = None
            class_registration = True

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> Any:
                return None

        # Defining the class triggers __init_subclass__ -> register_class
        # This uses the default register_class implementation.
        # It should call register_class on the registry.

        assert isinstance(DefaultRegClass.class_registry, MockRegistry)
        assert DefaultRegClass in DefaultRegClass.class_registry.registered  # type: ignore[unreachable]
        assert DefaultRegClass.class_registry.head_class == DefaultRegClass

    def test_subclass_registration(self) -> None:
        """Tests registration of a subclass where registry already exists and has a head class."""

        class Parent(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registry_type = MockRegistry
            class_registry = None
            class_registration = True

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> Any:
                return None

        class Child(Parent):
            class_registration = True

        # Child should be registered in Parent's registry
        assert Child in Parent.class_registry.registered  # type: ignore[attr-defined, union-attr, unused-ignore]
        # Parent.class_registry.head_class should remain Parent
        assert Parent.class_registry.head_class == Parent  # type: ignore[attr-defined, union-attr, unused-ignore]

    def test_register_class_no_registry(self) -> None:
        """Tests register_class when no registry is present."""

        class NoRegClass(self.UnitTestClass):  # type: ignore[name-defined, misc]
            class_registry = None
            class_registration = False

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> Any:
                return None

        # Should not raise error
        NoRegClass.register_class()
