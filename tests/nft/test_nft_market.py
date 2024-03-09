#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module implementing NFT Market unit tests """
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from kraken.nft import Market


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_spot_rest_contextmanager(nft_market: Market) -> None:
    """
    Checks if the client can be used as context manager.
    """
    with nft_market as market:
        result = market.get_nft(nft_id="NT4GUCU-SIJE2-YSQQG2", currency="USD")
        assert isinstance(result, dict)
        assert "nft" in result


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_nft(nft_market: Market) -> None:
    """
    Checks the ``get_nft`` endpoint
    """

    result = nft_market.get_nft(nft_id="NT4GUCU-SIJE2-YSQQG2", currency="USD")
    assert isinstance(result, dict)
    assert "nft" in result
    assert result["nft"].get("id") == "NT4GUCU-SIJE2-YSQQG2"


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_list_nfts(nft_market: Market) -> None:
    """
    Checks the ``list_nfts`` endpoint
    """

    result = nft_market.list_nfts(
        page_size=1,
        filter_="filter%5Bcollection_id%5D%3DNCQNABO-XYCA7-JMMSDF",
        sort="MostRelevant",
    )
    assert isinstance(result, dict)
    assert "total_items" in result


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_nft_provenance(nft_market: Market) -> None:
    """
    Checks the ``get_nft_provenance`` endpoint
    """

    result = nft_market.get_nft_provenance(nft_id="NT4GUCU-SIJE2-YSQQG2")
    assert isinstance(result, dict)


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_collection(nft_market: Market) -> None:
    """
    Checks the ``get_collection`` endpoint
    """

    result = nft_market.get_collection(
        collection_id="NCQNABO-XYCA7-JMMSDF",
        currency="USD",
    )
    assert isinstance(result, dict)


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_list_collections(nft_market: Market) -> None:
    """
    Checks the ``get_collection`` endpoint
    """

    result = nft_market.list_collections(
        page_size=1,
        currency="USD",
        filter_="filter%5Bsearch%5D=Williams",
        sort="MostRelevant",
    )
    assert isinstance(result, dict)
