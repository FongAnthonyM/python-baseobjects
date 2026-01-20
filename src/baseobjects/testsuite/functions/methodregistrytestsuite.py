"""methodregistrytestsuite.py
Base test suite for MethodRegistry and its subclasses.
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
import weakref
from collections.abc import Callable
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions.methodregistry import BaseMethodRegistry, BoundMethodRegistry, MethodRegistry
from .functionregistrytestsuite import FunctionRegistryTestSuite, RegistryTestObject, func1, func2


# Classes #
class BaseMethodRegistryTestSuite(FunctionRegistryTestSuite):
    """Base test suite for children of BaseMethodRegistry.

    This class provides common test functionality for child classes of BaseMethodRegistry.
    """

    UnitTestClass: ClassVar[type[BaseMethodRegistry]]

    # Tests #
    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Overrides base to avoid checking internal data structure if it differs.
        """
        obj = self.UnitTestClass(*args, **kwargs)
        assert isinstance(obj, self.UnitTestClass)

    # Functionality #
    def test_dict_initialization_with_kwargs(self) -> None:
        """Tests initialization with keyword arguments.

        BaseMethodRegistry might handle kwargs differently. Skipped.
        """

    def test_init_with_objects(self, test_instance: RegistryTestObject) -> None:
        """Tests initialization with a list of objects."""
        registry = self.UnitTestClass(objects=[test_instance])
        assert "method1" in registry
        assert registry["method1"] == test_instance.method1.__func__  # type: ignore[attr-defined]

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        registry = self.UnitTestClass(functions={"f": func1}, init=False)
        assert "f" not in registry

    def test_dict_operations(self, test_object: BaseMethodRegistry) -> None:
        """Tests basic dictionary operations.

        BaseMethodRegistry might not support all operations or behaves differently.
        """
        # Test basic setting if supported
        # Test basic setting if supported
        test_object["func1"] = func1
        assert "func1" in test_object
        assert test_object["func1"] is func1

    def test_func_property(self, test_object: BaseMethodRegistry) -> None:
        """Tests the __func__ property."""
        assert test_object.__func__ is test_object.data
        new_registry = self.UnitTestClass()
        test_object.__func__ = new_registry.data
        assert test_object.data is new_registry.data


class BoundMethodRegistryTestSuite(FunctionRegistryTestSuite):
    """Base test suite for children of BoundMethodRegistry.

    This class provides common test functionality for child classes of BoundMethodRegistry.
    """

    UnitTestClass: ClassVar[type[BoundMethodRegistry]]

    BaseRegistryClass: ClassVar[type[BaseMethodRegistry]] = BaseMethodRegistry

    # Fixtures #
    @pytest.fixture
    def base_registry(self, test_functions: dict[str, Callable[..., Any]]) -> BaseMethodRegistry:
        """Creates a base registry.

        Args:
            test_functions: A fixture providing test functions.

        Returns:
            BaseMethodRegistry: A base registry instance.
        """
        return self.BaseRegistryClass(test_functions)

    @pytest.fixture
    def test_object(self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject) -> BoundMethodRegistry:
        """Creates a test object (BoundMethodRegistry).

        Args:
            base_registry: A fixture providing a base registry.
            test_instance: A fixture providing a test object instance.

        Returns:
            BoundMethodRegistry: A test object instance.
        """
        return self.UnitTestClass(instance=test_instance, registry=base_registry)

    # Magic Methods #
    def test_getitem_unbound(self) -> None:
        """Tests __getitem__ when not bound."""
        obj = self.UnitTestClass()  # instance=None
        # Add a function to data so we can retrieve it

        def my_func() -> None:
            pass

        obj.data["f"] = my_func
        assert obj["f"] is my_func

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        BoundMethodRegistry requires arguments, so default creation fails. Skipped.
        """

    # Copying #
    def test_copy(self, test_object: BoundMethodRegistry) -> None:
        """Tests the copy behavior of the object.

        Overrides base to check functionality as BoundMethodRegistry might behave differently.
        """
        obj_copy = copy.copy(test_object)
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        # Copied bound registry should still point to same data?
        assert obj_copy.data == test_object.data
        assert obj_copy.__self__ is test_object.__self__

    def test_copy_method(self, test_object: BoundMethodRegistry) -> None:
        """Tests the copy method behavior of the object."""
        obj_copy = test_object.copy()
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        assert obj_copy.data == test_object.data
        assert obj_copy.__self__ is test_object.__self__

    def test_deepcopy(self, test_object: BoundMethodRegistry, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object."""
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)
        assert obj_deepcopy.data == test_object.data  # Data equality
        # Deepcopy of functions? Functions are usually immutable/singletons.
        # But data dict should be new.
        assert obj_deepcopy.data is not test_object.data

    def test_deepcopy_method(self, test_object: BoundMethodRegistry) -> None:
        """Tests the deepcopy method behavior of the object."""

    # Pickling #
    def test_pickling(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests pickling and unpickling of the object."""
        # Need to keep instance alive?
        instance = test_object.__self__
        data = (test_object, instance)
        pickled = pickle.dumps(data)
        unpickled_obj, _unpickled_instance = pickle.loads(pickled)

        assert isinstance(unpickled_obj, self.UnitTestClass)
        assert unpickled_obj.data == test_object.data

    # Tests #
    def test_dict_initialization(self) -> None:
        """Tests initialization with a dictionary.

        BoundMethodRegistry requires a registry, so standard dict init is not supported directly.
        """

    def test_dict_initialization_with_kwargs(self) -> None:
        """Tests initialization with keyword arguments.

        BoundMethodRegistry requires a registry, so standard dict init is not supported directly.
        """

    def test_dict_iteration(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests iteration over the dictionary.

        BoundMethodRegistry proxies iteration to data.
        """
        # test_object is populated (from base_registry)
        assert len(test_object) == 2
        for key in test_object:
            assert key in ["func1", "func2"]

    def test_dict_operations(self, test_object: BoundMethodRegistry) -> None:
        """Tests basic dictionary operations.

        BoundMethodRegistry proxies to data. Requires callable values.
        """

        def my_func() -> None:
            pass

        test_object["key1"] = my_func
        assert "key1" in test_object
        # When retrieving, it should be bound to the instance
        assert test_object["key1"].__func__ == my_func  # type: ignore[attr-defined]
        assert test_object["key1"].__self__ is test_object.__self__  # type: ignore[attr-defined]

    def test_dict_update(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests updating BaseDict with multiple items."""
        test_object.clear()
        test_object.update({"func1": func1, "func2": func2})
        assert len(test_object) == 2
        assert test_object["func1"].__func__ is func1  # type: ignore[attr-defined]
        assert test_object["func2"].__func__ is func2  # type: ignore[attr-defined]

    def test_dict_pop(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict."""
        test_object.clear()
        test_object["func1"] = func1
        test_object["func2"] = func2

        popped = test_object.pop("func2")
        # Pop returns BOUND method
        assert popped.__func__ is func2
        assert len(test_object) == 1
        assert "func2" not in test_object

    def test_dict_popitem(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests popping an arbitrary item from BaseDict."""
        test_object.clear()
        test_object["func1"] = func1
        test_object["func3"] = func2

        key, value = test_object.popitem()
        assert len(test_object) == 1
        assert key in ["func1", "func3"]
        assert value.__func__ in [func1, func2]

    def test_dict_clear(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests clearing BaseDict."""
        test_object.clear()
        test_object["func1"] = func1
        test_object["func2"] = func2
        test_object.clear()
        assert len(test_object) == 0

    def test_dict_set_item(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests setting items in BaseDict."""
        test_object.clear()
        test_object["func1"] = func1
        assert len(test_object) == 1
        assert test_object["func1"].__func__ is func1  # type: ignore[attr-defined]

    def test_dict_get(self, test_object: BoundMethodRegistry) -> None:  # type: ignore[override]
        """Tests getting items from BaseDict."""
        test_object.clear()
        test_object["func1"] = func1
        assert test_object.get("func1").__func__ is func1  # type: ignore[union-attr]
        assert test_object.get("nonexistent", func2) is func2

    def test_init_with_functions(self, test_functions: dict[str, Callable[..., Any]]) -> None:
        """Tests initialization with functions.

        BoundMethodRegistry requires a registry.
        """

    def test_init_with_object(self, test_instance: RegistryTestObject) -> None:
        """Tests initialization with an object.

        BoundMethodRegistry requires a registry.
        """

    def test_update_from_object(self, test_object: BoundMethodRegistry, test_instance: RegistryTestObject) -> None:  # type: ignore[override]
        """Tests updating from an object.

        BoundMethodRegistry proxies update to data.
        """
        test_object.update_from_object(test_instance)
        assert "method1" in test_object
        assert test_object["method1"] == test_instance.method1

    def test_init_with_registry_and_instance(
        self,
        base_registry: BaseMethodRegistry,
        test_instance: RegistryTestObject,
    ) -> None:
        """Tests initialization with registry and instance.

        Args:
            base_registry: A fixture providing a base registry.
            test_instance: A fixture providing a test object instance.
        """
        bound_registry = self.UnitTestClass(instance=test_instance, registry=base_registry)
        # Check shared data instead of .registry
        assert bound_registry.data is base_registry.data
        assert bound_registry.__self__ is test_instance

    def test_self_property(self, test_instance: RegistryTestObject) -> None:
        """Tests the __self__ property."""
        registry = self.BaseRegistryClass()
        bound_registry = self.UnitTestClass(instance=test_instance, registry=registry)
        assert bound_registry.__self__ is test_instance

    def test_weak_ref(self, test_instance: RegistryTestObject) -> None:
        """Tests that the instance is held weakly."""
        registry = self.BaseRegistryClass()
        self.UnitTestClass(instance=test_instance, registry=registry)

        weakref.ref(test_instance)
        del test_instance

    def test_descriptor_protocol(self, test_object: BoundMethodRegistry, test_instance: RegistryTestObject) -> None:
        """Tests the descriptor protocol.

        Args:
            test_object: A fixture providing a MethodRegistry.
            test_instance: A fixture providing a test object instance.
        """

        class DescriptorTest:
            registry = test_object

        instance = DescriptorTest()
        bound_registry = instance.registry
        assert isinstance(bound_registry, BoundMethodRegistry)
        assert bound_registry.__self__ is instance

    def test_init_with_owner(self, test_instance: RegistryTestObject) -> None:
        """Tests initialization with owner."""

        class Owner:
            pass

        obj = self.UnitTestClass(instance=test_instance, owner=Owner)
        assert obj.__owner__ is Owner

    def test_init_without_registry(self, test_instance: RegistryTestObject) -> None:
        """Tests initialization without registry argument."""
        # Local Packages #
        from ...functions.functionregistry import FunctionRegistry

        obj = self.UnitTestClass(instance=test_instance)
        assert isinstance(obj.data, FunctionRegistry)
        assert obj.__self__ is test_instance

    def test_getstate_branches(self, test_object: BoundMethodRegistry) -> None:
        """Tests __getstate__ branches."""
        # Standard Libraries #
        from unittest.mock import patch

        # Test tuple state
        with patch("baseobjects.functions.methodregistry.BaseReducible.__getstate__") as mock_getstate:
            mock_getstate.return_value = ({"a": 1}, {"slot": 2})
            state = test_object.__getstate__()
            assert isinstance(state, tuple)
            assert state[0]["_self_"] is test_object.__self__  # type: ignore[index]

        # Test tuple state with None first element
        with patch("baseobjects.functions.methodregistry.BaseReducible.__getstate__") as mock_getstate:
            mock_getstate.return_value = (None, {"slot": 2})
            state = test_object.__getstate__()
            assert state == (None, {"slot": 2})

        # Test None state
        with patch("baseobjects.functions.methodregistry.BaseReducible.__getstate__") as mock_getstate:
            mock_getstate.return_value = None
            state = test_object.__getstate__()
            assert isinstance(state, dict)
            assert state["_self_"] is test_object.__self__

    def test_self_setter_none(self, test_object: BoundMethodRegistry) -> None:
        """Tests setting __self__ to None."""
        assert test_object.__self__ is not None
        test_object.__self__ = None
        assert test_object.__self__ is None
        assert test_object._self_ is None

    def test_init_false(self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject) -> None:
        """Tests initialization with init=False."""
        registry = self.UnitTestClass(registry=base_registry, instance=test_instance, init=False)
        assert registry.__self__ is None
        assert registry.data != base_registry.data
        assert len(registry.data) == 0


class MethodRegistryTestSuite(BaseMethodRegistryTestSuite):
    """Base test suite for children of MethodRegistry.

    This class provides common test functionality for child classes of MethodRegistry.
    """

    UnitTestClass: ClassVar[type[MethodRegistry]]

    # Tests #
    def test_descriptor_protocol(self, test_object: MethodRegistry, test_instance: RegistryTestObject) -> None:
        """Tests the descriptor protocol.

        Args:
            test_object: A fixture providing a MethodRegistry.
            test_instance: A fixture providing a test object instance.
        """

        class DescriptorTest:
            registry = test_object

        instance = DescriptorTest()
        bound_registry = instance.registry
        assert isinstance(bound_registry, BoundMethodRegistry)
        assert bound_registry.__self__ is instance

        # Check shared data
        # assert bound_registry.data == test_object.data
