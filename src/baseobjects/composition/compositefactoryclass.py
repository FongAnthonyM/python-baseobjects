"""compositefactoryclass.py
A composite object that dispatches the original class with different components when a subclass is instantiated.
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
from inspect import signature, Parameter
from typing import Any, ClassVar

# Local Packages #
from ..classregistration import NamespaceClassRegistry, NamespaceRegisteredClass
from .basecomposite import BaseComposite


# Definitions #
# Constants #
_arg_only: set = {Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_ONLY}


# Classes #
class CompositeFactoryClass(BaseComposite, NamespaceRegisteredClass):
    """A composite object that dispatches its subclasses to a head class with different components.

    This class allows subclasses to act as presets for a head class. When a subclass is instantiated, it returns
    an instance of the head class (usually the first subclass that inherits from CompositeFactoryClass) configured
    with the components specified by the subclass.

    Class Attributes:
        class_registry_type: The type of registry to use for storing subclasses.
        class_registration: Determines if this class/subclass will be added to the registry.
    """

    # Class Attributes #
    class_registry_type: ClassVar[type[NamespaceClassRegistry]] = NamespaceClassRegistry
    class_registration: ClassVar[bool] = False
    init_parameters: ClassVar[dict[str, Parameter]] = {}
    init_args: ClassVar[tuple[str, ...]] = ()
    init_defaults: ClassVar[dict[str, Any]] = {}

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(
        cls,
        namespace: str | None = None,
        name: str | None = None,
        register_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """The init when creating a subclass.

        Args:
            namespace: The namespace to register the subclass under. If None, uses class_registry_namespace.
            name: The name to register the subclass as. If None, uses class_registry_name or class name.
            register_kwargs: Additional keyword arguments passed to the class registry during registration.
            **kwargs: Keyword arguments for creating a subclass.
        """
        super().__init_subclass__(namespace, name, register_kwargs, **kwargs)
        cls.init_parameters = dict(signature(cls.__init__).parameters)

        cls.init_defaults = {}
        init_args = []
        for arg, info in cls.init_parameters.items():
            if info.default is not Parameter.empty:
                cls.init_defaults[arg] = info.default
            if info.kind in _arg_only:
                init_args.append(arg)
        cls.init_args = tuple(init_args)

    @classmethod
    def build_head_class(
        cls,
        head_class: type[CompositeFactoryClass],
        *args: Any,
        **kwargs: Any,
    ) -> CompositeFactoryClass:
        """Builds the head class for this composite.

        Args:
            head_class: The head class to build.
            *args: Positional arguments for the component information.
            **kwargs: Keyword arguments for the component information.

        Returns:
            The head class instance.
        """
        component_types = cls.default_component_types | kwargs.pop("component_types", {})
        return head_class(*args, **({"component_types": component_types} | kwargs))

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """With the given input, will return the correct subclass."""
        if (
            cls.class_registry is not None
            and (head_class := cls.class_registry.head_class) is not None
            and head_class is not cls
        ):
            return cls.build_head_class(head_class, *args, **kwargs)
        return super().__new__(cls)
