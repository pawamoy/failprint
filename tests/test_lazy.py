"""Tests for the `runners` module."""

from failprint.lazy import LazyCallable, lazy


def test_decorating_function() -> None:
    """Test our `lazy` decorator."""

    @lazy
    def greet() -> None:
        ...  # pragma: no cover

    non_lazy = greet()
    assert isinstance(non_lazy, LazyCallable)
    assert not non_lazy.name

    @lazy(name="lazy_greet")
    def greet2() -> None:
        ...  # pragma: no cover

    non_lazy = greet2()
    assert isinstance(non_lazy, LazyCallable)
    assert non_lazy.name == "lazy_greet"


def test_lazifying_function() -> None:
    """Test our `lazy` decorator as a function."""

    def greet() -> None:
        ...  # pragma: no cover

    lazy_greet = lazy(greet)
    non_lazy = lazy_greet()
    assert isinstance(non_lazy, LazyCallable)
    assert not non_lazy.name

    lazy_greet = lazy(greet, name="lazy_greet")
    non_lazy = lazy_greet()
    assert isinstance(non_lazy, LazyCallable)
    assert non_lazy.name == "lazy_greet"
