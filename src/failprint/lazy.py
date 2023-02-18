"""This module contains a `lazy` decorator."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable


class LazyCallable:
    """This class allows users to create and pass lazy callables to the runner."""

    def __init__(self, call: Callable, args: tuple[Any], kwargs: dict[str, Any]) -> None:
        """Initialize a lazy callable.

        Parameters:
            call: The origin callable.
            args: The `*args` to pass when calling.
            kwargs: The `**kwargs` to pass when calling.
        """
        self.call = call
        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> Any:  # noqa: D102
        return self.call(*self.args, **self.kwargs)


def lazy(call: Callable) -> Callable:
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

    Returns:
        A lazy callable instance.
    """

    @wraps(call)  # noqa: WPS430
    def lazy_caller(*args, **kwargs):  # noqa: WPS430
        return LazyCallable(call, args, kwargs)

    return lazy_caller
