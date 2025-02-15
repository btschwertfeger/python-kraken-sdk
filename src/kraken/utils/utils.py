# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module implementing utility functions used across the package"""

from __future__ import annotations

import warnings
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


def deprecated(message: str) -> Callable:
    """
    Function used as decorator to mark decorated functions as deprecated with a
    custom message.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            *args: Any | None,
            **kwargs: Any | None,
        ) -> Any | None:  # noqa: ANN401
            warnings.warn(
                f"{message}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["deprecated"]
