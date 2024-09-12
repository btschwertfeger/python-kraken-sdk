#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module implementing unit tests related to NFT Trade"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from kraken.nft import Trade

from datetime import datetime, timedelta

from kraken.exceptions import (
    KrakenInvalidArgumentBelowMinError,
    KrakenInvalidArgumentOfferNotFoundError,
    KrakenNFTNotAvailableError,
)


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_contextmanager(nft_auth_trade: Trade) -> None:
    """
    Checks if the clients can be used as context manager.
    """
    with nft_auth_trade as trade:
        result = trade.get_nft_wallet()
        assert isinstance(result, dict)


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_create_auction(nft_auth_trade: Trade) -> None:
    """Checks the ``create_auction`` endpoint."""

    with pytest.raises(KrakenNFTNotAvailableError):
        nft_auth_trade.create_auction(
            auction_currency="ETH",
            nft_id=["NT4EFBO-OWGI5-QLO7AG"],
            auction_type="fixed",
            auction_params={
                "allow_offers": True,
                "ask_price": 100000,
                "expire_time": int((datetime.now() + timedelta(days=11)).timestamp()),
            },
            start_time=int((datetime.now() + timedelta(days=10)).timestamp()),
        )


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_modify_auction(nft_auth_trade: Trade) -> None:
    """
    Checks the ``modify_auction`` endpoint.
    It is sufficient here to check that the request is valid, even if the
    auction is not valid.
    """

    response = nft_auth_trade.modify_auction(
        auction_id="AT2POJ-4CH3O-4TH6JH",
        ask_price="0.3",
    )
    assert isinstance(response, dict)
    assert response.get(
        "error",
        [],
    ) == ["EAPI:Invalid arguments:No auction with the provided ID"]


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_cancel_auction(nft_auth_trade: Trade) -> None:
    """Checks the ``cancel_auction`` endpoint."""

    result = nft_auth_trade.cancel_auction(auction_ids=["AT2POJ-4CH3O-4TH6JH"])

    assert isinstance(result, dict)
    assert "statuses" in result
    assert isinstance(result["statuses"], list)
    assert len(result["statuses"]) == 1
    assert isinstance(result["statuses"][0], dict)
    assert result["statuses"][0].get("id") == "AT2POJ-4CH3O-4TH6JH"
    assert result["statuses"][0].get("status") == "failed"
    assert result["statuses"][0].get("reason") == "not found"


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
@pytest.mark.skip(reason="CI should not play with NFTs")
def test_nft_trade_place_offer(nft_auth_trade: Trade) -> None:
    """Checks the ``place_offer`` endpoint."""

    with pytest.raises(KrakenInvalidArgumentBelowMinError):
        nft_auth_trade.place_offer(
            nft_id=["NTYI3JW-MH6TV-FIHLVZ"],
            offer_amount=1,
            offer_currency="MATIC",
        )


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
@pytest.mark.skip(reason="CI should not play with NFTs")
def test_nft_trade_counter_offer(nft_auth_trade: Trade) -> None:
    """Checks the ``counter_offer`` endpoint."""

    with pytest.raises(KrakenInvalidArgumentOfferNotFoundError):
        nft_auth_trade.counter_offer(
            currency="MATIC",
            ask_price=1,
            offer_id="ONQYPLG-OFARL-35RBGO",
        )


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
@pytest.mark.skip(reason="CI should not play with NFTs")
def test_nft_trade_accept_offer(nft_auth_trade: Trade) -> None:
    """Checks the ``accept_offer`` endpoint."""
    # THIS IS DANGEROUS - SKIP!
    with pytest.raises(KrakenInvalidArgumentOfferNotFoundError):
        nft_auth_trade.accept_offer(offer_id="ONQYPLG-OFARL-35RBG-O")


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_get_auction_trades(nft_auth_trade: Trade) -> None:
    """Checks the ``get_auction_trades`` endpoint."""

    result = nft_auth_trade.get_auction_trades()

    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert "auction_id" in result[0]
    assert "trade_id" in result[0]
    assert "currency" in result[0]


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_get_user_offers(nft_auth_trade: Trade) -> None:
    """Checks the ``get_user_offers`` endpoint."""

    result = nft_auth_trade.get_user_offers(
        pos=1,
        scope="placed",
        sort="asc",
        chain=["MATIC"],
        exclude_quotes=True,
        status="open",
        count=10,
        collection=["NCQNABO-XYCA7-JMMSDF"],
    )

    assert isinstance(result, dict)
    assert "offers" in result
    assert "count" in result
    assert isinstance(result["offers"], list)


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_get_nft_wallet(nft_auth_trade: Trade) -> None:
    """Checks the ``get_nft_wallet`` endpoint."""

    result = nft_auth_trade.get_nft_wallet(
        chain="MATIC",
        currency="USD",
        page=1,
        per_page=5,
        custody="Kraken",
        price_currency="USD",
        price_high=5,
        price_low=1,
        search=" Williams Racing Collectibles+ Grid Pass",
        sort="RecentlyBought",
        status="BuyNow",
    )

    assert isinstance(result, dict)
    assert "items" in result
    assert isinstance(result["items"], list)


@pytest.mark.nft
@pytest.mark.nft_auth
@pytest.mark.nft_trade
def test_nft_trade_list_nft_transactions(nft_auth_trade: Trade) -> None:
    """Checks the ``list_nft_transactions`` endpoint."""

    result = nft_auth_trade.list_nft_transactions(
        page=1,
        per_page=5,
        sort="desc",
        nft_id="NTRU2ZH-EK7SW-QHJOVI",
        type_="Claim",
    )

    assert isinstance(result, dict)
    assert "items" in result
    assert isinstance(result["items"], list)
    assert len(result["items"]) > 0
    assert isinstance(result["items"][0], dict)
    assert "nft_id" in result["items"][0]
    assert result["items"][0]["nft_id"] == "NTRU2ZH-EK7SW-QHJOVI"
