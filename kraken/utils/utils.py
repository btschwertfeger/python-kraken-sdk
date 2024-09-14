#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module implementing utility functions used across the package"""

from __future__ import annotations

import warnings
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


def deprecated(func: Callable) -> Callable:
    """
    Function used as decorator to mark decorated functions as deprecated.
    """

    @wraps(func)
    def wrapper(
        *args: Any | None,
        **kwargs: Any | None,
    ) -> Any | None:  # noqa: ANN401
        warnings.warn(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return wrapper


__all__ = ["deprecated"]
