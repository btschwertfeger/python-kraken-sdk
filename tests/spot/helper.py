#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

from typing import Any, Union


def is_not_error(value: Union[dict, Any]) -> bool:
    """Returns True if 'error' in dict."""
    return isinstance(value, dict) and "error" not in value
