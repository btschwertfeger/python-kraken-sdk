#!/usr/bin/env python
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
        filter_="filter[collection_id]=NCQNABO-XYCA7-JMMSDF",
        sort="MostRelevant",
    )
    assert isinstance(result, dict)
    assert "total_items" in result
    assert "cursor" in result
    assert "items" in result


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_nft_provenance(nft_market: Market) -> None:
    """
    Checks the ``get_nft_provenance`` endpoint
    """

    result = nft_market.get_nft_provenance(nft_id="NT4GUCU-SIJE2-YSQQG2")
    assert isinstance(result, dict)
    assert "items" in result
    assert result.get("total") == 1
    assert result["items"][0]["nft_id"] == "NT4GUCU-SIJE2-YSQQG2"


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
    assert "collection" in result
    assert result["collection"]["id"] == "NCQNABO-XYCA7-JMMSDF"
    assert result["collection"]["name"] == "Williams Racing Collectibles+ Grid Pass"


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_list_collections(nft_market: Market) -> None:
    """
    Checks the ``list_collections`` endpoint
    """

    result = nft_market.list_collections(
        page_size=1,
        currency="USD",
        filter_="filter[search]=Williams",
        sort="MostRelevant",
    )
    assert isinstance(result, dict)
    assert "total_items" in result
    assert "cursor" in result
    assert "items" in result


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_creator(nft_market: Market) -> None:
    """
    Checks the ``get_creator`` endpoint
    """

    result = nft_market.get_creator(creator_id="NA7NELE-FOQFZ-ODWOTV")
    assert isinstance(result, dict)
    assert "creator" in result
    assert result["creator"].get("id") == "NA7NELE-FOQFZ-ODWOTV"


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_list_creators(nft_market: Market) -> None:
    """
    Checks the ``list_creators`` endpoint
    """

    result = nft_market.list_creators(
        page_size=1,
        currency="USD",
        filter_="filter[collection_search]=Williams",
        sort="MostRelevant",
    )
    assert isinstance(result, dict)
    assert "total_items" in result
    assert "cursor" in result
    assert "items" in result


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_list_blockchains(nft_market: Market) -> None:
    """
    Checks the ``list_blockchains`` endpoint
    """

    result = nft_market.list_blockchains()
    assert isinstance(result, dict)
    assert "items" in result
    assert "total" in result
    assert result["total"] >= 3


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_auctions(nft_market: Market) -> None:
    """
    Checks the ``get_auctions`` endpoint
    """
    result = nft_market.get_auctions(
        status="closed",
        filter_="nft_id[]=NTN63WS-PBAV3-FQDQDG",
    )
    assert isinstance(result, list)
    assert len(result) != 0
    assert isinstance(result[0], dict)
    assert result[1]["status_detail"] == "CLOSED"


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_offers(nft_market: Market) -> None:
    """
    Checks the ``get_offers`` endpoint
    """
    result = nft_market.get_offers(nft_id="NT4GUCU-SIJE2-YSQQG2")
    assert isinstance(result, dict)
    assert "offers" in result
    assert isinstance(result["offers"], list)


@pytest.mark.nft()
@pytest.mark.nft_market()
def test_nft_get_nft_quotes(nft_market: Market) -> None:
    """
    Checks the ``get_nft_quotes`` endpoint
    """
    result = nft_market.get_nft_quotes(
        filter_="nft_id[]=NT4GUCU-SIJE2-YSQQG2",
        count=1,
    )
    assert isinstance(result, dict)
    assert "NT4GUCU-SIJE2-YSQQG2" in result
    assert isinstance(result["NT4GUCU-SIJE2-YSQQG2"], list)
