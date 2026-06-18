# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2026 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Offline unit tests for the shared Spot base client logic: request signing, the
``ensure_string`` decorator, the error handler, and the small helpers. None of
these touch the network or require API credentials.
"""

from __future__ import annotations

import base64
from typing import Self

import pytest

from kraken.base_api import ErrorHandler, SpotClient, defined, ensure_string
from kraken.exceptions import KrakenInsufficientFundsError

# A synthetic, base64-decodable secret built at runtime. It is not a real key;
# it only has to be valid base64 so the HMAC signing can decode it.
TEST_SECRET = base64.b64encode(b"python-kraken-sdk unit-test secret value").decode()


@pytest.mark.unit
@pytest.mark.spot
class TestSpotBaseAPIUnit:
    """Offline unit tests for :class:`kraken.base_api.SpotClient`."""

    def test_defined(self: Self) -> None:
        """``defined`` is a plain ``is not None`` check."""
        assert defined(0) is True
        assert defined("") is True
        assert defined([]) is True
        assert defined(None) is False

    def test_ensure_string_joins_list(self: Self) -> None:
        """A list argument is collapsed into a comma-joined string."""

        @ensure_string("assets")
        def echo(assets: str | list[str] | None = None) -> str | None:
            return assets

        assert echo(assets=["XBT", "ETH", "USD"]) == "XBT,ETH,USD"

    def test_ensure_string_passes_through_str_and_none(self: Self) -> None:
        """Strings and ``None`` are forwarded unchanged."""

        @ensure_string("assets")
        def echo(assets: str | list[str] | None = None) -> str | None:
            return assets

        assert echo(assets="XBT,ETH") == "XBT,ETH"
        assert echo(assets=None) is None
        assert echo() is None

    def test_ensure_string_rejects_unsupported_type(self: Self) -> None:
        """An unsupported type raises ``TypeError``."""

        @ensure_string("assets")
        def echo(assets: str | list[str] | None = None) -> str | None:
            return assets

        with pytest.raises(TypeError, match=r"assets can't be"):
            echo(assets=123)  # type: ignore[arg-type]

    def test_ensure_string_jsonifies_extra_params(self: Self) -> None:
        """The ``extra_params`` argument is json-dumped instead of joined."""

        @ensure_string("extra_params")
        def echo(extra_params: str | dict | None = None) -> str | None:
            return extra_params

        assert (
            echo(extra_params={"foo": "bar", "count": 1})
            == '{"foo": "bar", "count": 1}'
        )

    def test_ensure_string_extra_params_must_be_dict(self: Self) -> None:
        """A non-dict ``extra_params`` raises ``TypeError``."""

        @ensure_string("extra_params")
        def echo(extra_params: str | dict | None = None) -> str | None:
            return extra_params

        with pytest.raises(TypeError, match=r"extra_params must be type dict"):
            echo(extra_params=["not", "a", "dict"])  # type: ignore[arg-type]

    def test_signature_matches_golden_value(self: Self) -> None:
        """
        The Spot signature is HMAC-SHA512 over ``url_path`` plus the SHA256 of
        ``nonce + data``. Pin a known input/output pair so a regression in the
        signing path is caught.
        """
        client = SpotClient(secret=TEST_SECRET)
        signature: str = client._get_kraken_signature(
            url_path="/0/private/AddOrder",
            data="nonce=1616492376594&ordertype=limit&pair=XBTUSD",
            nonce=1616492376594,
        )
        assert signature == (
            "Fo+0Uhanvs3F1byZFCjVBMLsCcRE2xLQMDpoA3Q9hawoZ0ZL35AmbknAQBlOIs4baRx9UGhzQH+/CTl9qnyp1w=="  # codespell:ignore
        )

    def test_signature_changes_with_nonce(self: Self) -> None:
        """Holding the data fixed, a different nonce yields a different signature."""
        client = SpotClient(secret=TEST_SECRET)
        data = "ordertype=limit&pair=XBTUSD"
        first: str = client._get_kraken_signature(
            url_path="/0/private/Balance",
            data=data,
            nonce=1,
        )
        second: str = client._get_kraken_signature(
            url_path="/0/private/Balance",
            data=data,
            nonce=2,
        )
        assert first != second

    def test_error_handler_returns_result_on_success(self: Self) -> None:
        """An empty ``error`` list returns the ``result`` payload."""
        handler = ErrorHandler()
        assert handler.check({"error": [], "result": {"balance": "1.0"}}) == {
            "balance": "1.0",
        }

    def test_error_handler_raises_typed_exception(self: Self) -> None:
        """A known error string raises the mapped Kraken exception."""
        handler = ErrorHandler()
        with pytest.raises(KrakenInsufficientFundsError):
            handler.check({"error": ["EOrder:Insufficient funds"]})

    def test_error_handler_returns_data_on_unknown_error(self: Self) -> None:
        """An unmapped error string is returned as-is instead of raising."""
        handler = ErrorHandler()
        data: dict = {"error": ["EService:Totally unmapped error"]}
        assert handler.check(data) == data

    def test_get_nonce_is_increasing_numeric_string(self: Self) -> None:
        """The nonce is a numeric string that does not decrease over time."""
        client = SpotClient()
        first: str = client.get_nonce()
        second: str = client.get_nonce()
        assert first.isdigit()
        assert second.isdigit()
        assert int(second) >= int(first)

    def test_return_unique_id(self: Self) -> None:
        """``return_unique_id`` is a 32-character hex string, unique per call."""
        client = SpotClient()
        first: str = client.return_unique_id
        second: str = client.return_unique_id
        assert len(first) == 32
        assert all(char in "0123456789abcdef" for char in first)
        assert first != second
