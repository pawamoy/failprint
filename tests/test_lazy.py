# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Tests for the `runners` module."""

from failprint._internal.lazy import LazyCallable, lazy


def test_decorating_function() -> None:
    """Test our `lazy` decorator."""

    @lazy
    def greet() -> None: ...  # pragma: no cover

    non_lazy = greet()
    assert isinstance(non_lazy, LazyCallable)
    assert not non_lazy.name

    @lazy(name="lazy_greet")
    def greet2() -> None: ...  # pragma: no cover

    non_lazy = greet2()
    assert isinstance(non_lazy, LazyCallable)
    assert non_lazy.name == "lazy_greet"


def test_lazifying_function() -> None:
    """Test our `lazy` decorator as a function."""

    def greet() -> None: ...  # pragma: no cover

    lazy_greet = lazy(greet)
    non_lazy = lazy_greet()
    assert isinstance(non_lazy, LazyCallable)
    assert not non_lazy.name

    lazy_greet = lazy(greet, name="lazy_greet")
    non_lazy = lazy_greet()
    assert isinstance(non_lazy, LazyCallable)
    assert non_lazy.name == "lazy_greet"
