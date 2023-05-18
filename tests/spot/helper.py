#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

from typing import Any


def is_not_error(value: Any) -> bool:
    """Returns True if 'error' in dict."""
    return isinstance(value, dict) and "error" not in value
