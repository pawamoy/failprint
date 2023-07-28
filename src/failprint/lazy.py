"""This module contains a `lazy` decorator."""

from __future__ import annotations

import sys
import warnings
from functools import wraps
from typing import Callable, Generic, TypeVar, overload

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")


class LazyCallable(Generic[_R]):
    """This class allows users to create and pass lazy callables to the runner."""

    def __init__(self, call: Callable[_P, _R], args: tuple, kwargs: dict, name: str | None = None) -> None:
        """Initialize a lazy callable.

        Parameters:
            call: The origin callable.
            args: The `*args` to pass when calling.
            kwargs: The `**kwargs` to pass when calling.
            name: The name of the callable.
        """
        self.call = call
        self.args = args
        self.kwargs = kwargs
        self.name = name

    def __call__(self) -> _R:  # noqa: D102
        return self.call(*self.args, **self.kwargs)


def _lazy(call: Callable[_P, _R], name: str | None = None) -> Callable[_P, LazyCallable]:
    @wraps(call)
    def lazy_caller(*args: _P.args, **kwargs: _P.kwargs) -> LazyCallable:
        return LazyCallable(call, args, kwargs, name=name)

    return lazy_caller


_FunctionType = Callable[_P, _R]
_DecoratorType = Callable[[_FunctionType], Callable[_P, LazyCallable]]


@overload
def lazy(call: Callable[_P, _R], name: str | None = None) -> Callable[_P, LazyCallable]:
    ...  # pragma: no cover


@overload
def lazy(call: None = None, name: str | None = None) -> _DecoratorType:
    ...  # pragma: no cover


def lazy(call: Callable[_P, _R] | None = None, name: str | None = None) -> Callable[_P, LazyCallable] | _DecoratorType:
    """Transform a callable into a lazy callable.

    Being able to create a lazy callable improves the UX/DX.
    Instead of having to pass `args` and `kwargs` to the runner,
    one can now call the function directly, enjoying auto-completion
    and other editor features. Before:

    ```python
    from failprint.runners import run


    def greet(name):
        return f"hello {name}"


    run(greet, args=["tim"])
    ```

    After:

    ```python
    from failprint.runners import run
    from failprint.lazy import lazy


    @lazy
    def greet(name):
        return f"hello {name}"


    run(greet("tim"))
    ```

    Parameters:
        call: The callable to lazify.
        name: An optional name to give to the new callable.

    Returns:
        A lazy callable instance.
    """
    if name is None and isinstance(call, str):
        call, name = name, call
        warnings.warn(
            "Passing a name as positional argument is deprecated. Use a keyword argument instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    if call is None:

        def decorator(func: _FunctionType) -> _FunctionType:
            return _lazy(func, name)

        return decorator

    return _lazy(call, name)


__all__ = ["lazy", "LazyCallable"]
