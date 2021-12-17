#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any, Optional, Tuple

# Third-Party Packages #

# Local Packages #
from ..bases import BaseMeta


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created.

    Args:
        name: The name of this class.
        bases: The parent types of this class.
        namespace: The methods and class attributes of this class.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name: str, bases: Tuple[type, ...], namespace: dict[str, Any]) -> None:
        super().__init__(name, bases, namespace)
        cls._init_class_(name, bases, namespace)

    def _init_class_(cls,
                     name: Optional[str] = None,
                     bases: Optional[Tuple[type, ...]] = None,
                     namespace: Optional[dict[str, Any]] = None) -> None:
        pass
