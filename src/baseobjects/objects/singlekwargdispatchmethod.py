#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" singlekwargdispatchmethod.py
A circular doubly linked container which is a fast and efficient way to store ordered data, especially if constantly
changes size.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from functools import singledispatch, singledispatchmethod, update_wrapper
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..types_ import AnyCallable, AnyCallableType


# Definitions #
# Classes #
class singlekwargdispatchmethod(singledispatchmethod):
    def __init__(self, arg: AnyCallable | str, func: AnyCallable | None = None) -> None:
        self.dispatcher: singledispatch | None = None
        self.func: AnyCallable | None = None
        self._kwarg: str | None = None
        self.parse: AnyCallableType = self.parse_first

        if isinstance(arg, str):
            self.construct(kwarg=arg, func=func)
        else:
            self.construct(func=func)

    @property
    def kwarg(self) -> str:
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    def construct(self, kwarg: str | None = None, func: AnyCallable | None = None) -> None:
        if kwarg is not None:
            self.kwarg = kwarg

        if func is not None:
            if not callable(func) and not hasattr(func, "__get__"):
                raise TypeError(f"{func!r} is not callable or a descriptor")

            self.dispatcher = singledispatch(func)
            self.func = func

    def __call__(self, func: AnyCallable | None = None) -> None:
        self.construct(func=func)

    def set_kwarg(self, kwarg: str | None) -> None:
        if kwarg is None:
            self.parse = self.parse_first
        else:
            self.parse = self.parse_kwarg
        self.kwarg = kwarg

    def parse_first(self, *args: Any, **kwargs: Any) -> type[Any]:
        if args:
            return args[0].__class__
        else:
            return next(iter(kwargs.values())).__class__

    def parse_kwarg(self, *args: Any, **kwargs: Any) -> type[Any]:
        return kwargs[self._kwarg].__class__

    def __get__(self, obj: Any, cls: type[Any] | None = None) -> AnyCallable:
        def _method(*args: Any, **kwargs: Any) -> Any:
            type_ = self.parse(*args, **kwargs)
            method = self.dispatcher.dispatch(type_)
            return method.__get__(obj, cls)(*args, **kwargs)

        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.register = self.register
        _method.set_kwarg = self.set_kwarg
        update_wrapper(_method, self.func)
        return _method
