"""Tests for the `capture` module."""

import pytest

from failprint.capture import Capture, cast_capture


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
def test_cast_string(value, expected):
    """
    Cast various values in a Capture enumeration value.

    Arguments:
        value: The value to cast.
        expected: The value to expect.
    """
    assert cast_capture(value) == expected
