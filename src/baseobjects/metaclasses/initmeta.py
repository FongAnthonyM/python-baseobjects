"""initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
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

# Local Packages #
from ..bases import BaseMeta


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created.

    Args:
        name: The name of this class.
        bases: The parent types of this class.
        namespace: The functions and class attributes of this class.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        """Initialize the metaclass and invoke class initialization hook.

        Args:
            name: The name of the class being created.
            bases: The base classes of the class being created.
            namespace: The attribute dictionary of the class being created.
        """
        super().__init__(name, bases, namespace)
        self._init_class_(name=name, bases=bases, namespace=namespace)

    def _init_class_(
        self,
        name: str | None = None,
        bases: tuple[type, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        """The init class method for this object.

        Args:
            name: The name of this class.
            bases: The parent types of this class.
            namespace: The functions and class attributes of this class.
        """
