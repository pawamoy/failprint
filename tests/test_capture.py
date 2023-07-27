"""Tests for the `capture` module."""

from __future__ import annotations

import pytest

from failprint.capture import Capture


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("stdout", Capture.STDOUT),
        ("stderr", Capture.STDERR),
        ("both", Capture.BOTH),
        ("none", Capture.NONE),
        (True, Capture.BOTH),
        (False, Capture.NONE),
        (Capture.STDOUT, Capture.STDOUT),
        (Capture.STDERR, Capture.STDERR),
        (Capture.BOTH, Capture.BOTH),
        (Capture.NONE, Capture.NONE),
        (None, Capture.BOTH),  # default
    ],
)
def test_cast_string(value: str | bool | Capture, expected: Capture) -> None:
    """Cast various values in a Capture enumeration value.

    Arguments:
        value: The value to cast.
        expected: The value to expect.
    """
    assert Capture.cast(value) == expected
