#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that checks the general Spot Base API class."""

import pytest

from kraken.base_api import KrakenBaseSpotAPI
from kraken.exceptions import KrakenException


@pytest.mark.spot
def test_KrakenBaseSpotAPI_without_exception() -> None:
    """
    Checks first if the expected error will be raised and than
    creates a new KrakenBaseSpotAPI instance that do not raise
    the custom Kraken exceptions. This new instance thant executes
    the same request and the returned response gets evaluated.
    """
    with pytest.raises(KrakenException.KrakenInvalidAPIKeyError):
        KrakenBaseSpotAPI(
            key="fake",
            secret="fake",
        )._request(method="POST", uri="/private/AddOrder", auth=True)

    assert KrakenBaseSpotAPI(
        key="fake", secret="fake", use_custom_exceptions=False
    )._request(method="POST", uri="/private/AddOrder", auth=True).json() == {
        "error": ["EAPI:Invalid key"]
    }
