"""Deprecated. Import from `failprint` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from failprint._internal import runners


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `failprint.runners` is deprecated. Import from `failprint` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(runners, name)
