"""basecomponenttestsuite.py
Base test suite for BaseComponent and its subclasses.
"""

# Header #
__package_name__ = "Anys"

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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...composition import BaseComponent
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseComponentTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseComponent.

    This class provides common test functionality for child classes of BaseComponent, including tests for composite
    relationships. Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestComposite: type[Any]

    UnitTestClass: type[BaseComponent]

    # Fixtures #
    @pytest.fixture
    def test_composite(self, *args: Any, **kwargs: Any) -> Any:
        """Creates a test composite object.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            A test composite object instance.
        """
        return self.UnitTestComposite()

    @pytest.fixture
    def test_object(self, test_composite: Any, *args: Any, **kwargs: Any) -> BaseComponent:
        """Creates a test object.

        Args:
            test_composite: A fixture providing a test composite object.
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            Any: A test object instance.
        """
        return self.UnitTestClass(test_composite, *args, **kwargs)

    # Tests #
    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: Any, method: str) -> None:  # type: ignore[override, unused-ignore]
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        assert obj_copy.composite is test_object.composite

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(self, test_object: Any, method: str, memo: dict[Any, Any] | None = None) -> None:  # type: ignore[override, unused-ignore]
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)
        if test_object.composite is not None:
            assert obj_deepcopy.composite is not test_object.composite
            assert isinstance(obj_deepcopy.composite, type(test_object.composite))

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:  # type: ignore[override, unused-ignore]
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        if getattr(test_object, "composite", None) is not None:
            # If the object has a composite, we need to pickle both to keep the composite alive
            # because the component only holds a weak reference.
            items = (test_object, test_object.composite)
            pickled = pickle.dumps(items)
            unpickled_items = pickle.loads(pickled)
            unpickled = unpickled_items[0]
        else:
            pickled = pickle.dumps(test_object)
            unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)
        if getattr(test_object, "composite", None) is not None:
            assert unpickled.composite is not test_object.composite
            assert isinstance(unpickled.composite, type(test_object.composite))

    # Functionality #
    def test_composite_property(self, test_composite: Any) -> None:
        """Tests the composite property of the component.

        This test verifies that the composite property correctly gets and sets the composite object.

        Args:
            test_composite: A fixture providing a composite object.
        """
        # Test initial composite value
        test_object = self.UnitTestClass(test_composite)
        assert test_object.composite is test_composite

        # Test setting new composite
        new_composite = self.UnitTestComposite()
        test_object.composite = new_composite
        assert test_object.composite is new_composite

        # Test setting None
        test_object.composite = None
        assert test_object.composite is None

    def test_composite_weakref(self, test_composite: Any) -> None:
        """Tests that the composite reference is a weak reference.

        This test verifies that the component holds a weak reference to its composite, which means
        the composite can be garbage collected even if the component still exists.

        Args:
            test_composite: A fixture providing a composite object.
        """
        # Verifies the composite reference is a weak reference
        test_object = self.UnitTestClass(test_composite)
        assert isinstance(test_object._composite, weakref.ReferenceType)

        # Verifies we can still access the composite through the property
        assert test_object.composite is test_composite

        # Creates a new scope to test garbage collection
        def temp_scope() -> None:
            temp_composite = self.UnitTestComposite()
            test_object.composite = temp_composite

        # Gets weak reference to temporary composite
        temp_scope()

        # Verifies the temporary composite was garbage collected
        assert test_object.composite is None

    def test_composite_none(self) -> None:
        """Tests creating a component with no composite."""
        test_object = self.UnitTestClass()
        assert test_object.composite is None

    def test_composite_set_none(self, test_object: BaseComponent) -> None:
        """Tests setting the composite to None.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.composite = None
        assert test_object.composite is None
        assert test_object._composite is None

    def test_construct_with_composite(self, test_composite: Any) -> None:
        """Tests constructing with a composite.

        Args:
            test_composite: A fixture providing a composite object.
        """
        test_object = self.UnitTestClass()
        test_object.construct(composite=test_composite)
        assert test_object.composite is test_composite
