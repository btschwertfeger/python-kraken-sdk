#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that checks the general Futures Base API class."""


import pytest

from kraken.base_api import KrakenBaseFuturesAPI
from kraken.exceptions import KrakenException


@pytest.mark.futures
def test_KrakenBaseFuturesAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than
    creates a new KrakenBaseFuturesAPI instance that do not raise
    the custom Kraken exceptions. This new instance thant executes
    the same request and the returned response gets evaluated.
    """
    with pytest.raises(KrakenException.KrakenRequiredArgumentMissingError):
        KrakenBaseFuturesAPI(
            key="fake",
            secret="fake",
        )._request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)

    result: dict = (
        KrakenBaseFuturesAPI(key="fake", secret="fake", use_custom_exceptions=False)
        ._request(method="POST", uri="/derivatives/api/v3/sendorder", auth=True)
        .json()
    )

    assert (
        result.get("result") == "error"
        and result.get("error") == "requiredArgumentMissing"
    )
