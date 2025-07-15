"""Deprecated. Import from `failprint` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from failprint._internal import debug


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `failprint.debug` is deprecated. Import from `failprint` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(debug, name)
