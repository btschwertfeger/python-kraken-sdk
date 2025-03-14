# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module implementing utility functions used across the package"""

from __future__ import annotations

import warnings
from enum import Enum, auto
from functools import wraps
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


class WSState(Enum):
    """Enum class representing the state of the WebSocket connection"""

    INIT = auto()  # Initial state
    CONNECTING = auto()  # Connection is being established
    CONNECTED = auto()  # Connection is established
    RECONNECTING = auto()  # Connection is being re-established
    CANCELLING = auto()  # Connection is being cancelled
    ERRORHANDLING = auto()  # Error is being handled
    ERROR = auto()  # Error occurred
    CLOSED = auto()  # Connection is closed


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
