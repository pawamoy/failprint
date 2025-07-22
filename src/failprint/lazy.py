"""Deprecated. Import from `failprint` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from failprint._internal import lazy as lazy_module


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `failprint.lazy` is deprecated. Import from `failprint` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(lazy_module, name)
