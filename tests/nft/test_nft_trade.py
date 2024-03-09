#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger


from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from kraken.nft import Trade

from .helper import is_not_error


@pytest.mark.nft()
@pytest.mark.nft_trade()
@pytest.mark.spot_auth()
def test_nft_trade_contextmanager(nft_trade: Trade) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with nft_trade as trade:
        result = trade.get_assets()
        assert is_not_error(result), result
