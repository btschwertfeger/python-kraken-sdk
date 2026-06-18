# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2026 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""
Offline unit tests for the shared Futures base client logic: request signing
and the Futures-specific ``sendStatus`` / ``batchStatus`` error handling. None
of these touch the network or require API credentials.
"""

from __future__ import annotations

import base64
from typing import Self

import pytest

from kraken.base_api import ErrorHandler, FuturesClient
from kraken.exceptions import KrakenRequiredArgumentMissingError

# A synthetic, base64-decodable secret built at runtime. It is not a real key;
# it only has to be valid base64 so the HMAC signing can decode it.
TEST_SECRET = base64.b64encode(b"python-kraken-sdk unit-test secret value").decode()


@pytest.mark.unit
@pytest.mark.futures
class TestFuturesBaseAPIUnit:
    """Offline unit tests for :class:`kraken.base_api.FuturesClient`."""

    def test_signature_matches_golden_value(self: Self) -> None:
        """
        The Futures signature is HMAC-SHA512 over the SHA256 of
        ``data + nonce + endpoint``. Pin a known input/output pair so a
        regression in the signing path is caught.
        """
        client = FuturesClient(secret=TEST_SECRET)
        signature: str = client._get_kraken_futures_signature(
            endpoint="/derivatives/api/v3/sendorder",
            data="orderType=lmt&symbol=PI_XBTUSD",
            nonce="1616492376594",
        )
        assert signature == (
            "Txi+gJVXe3EN1brXYQ46FuV6UVtEVSKhc6dYMhPb7a/HXZLGvO6m9UUg+KVKqhLxrbllOPI7qRkHYmPfJZZSGA=="
        )

    def test_signature_strips_derivatives_prefix(self: Self) -> None:
        """
        The ``/derivatives`` prefix is removed before signing, so both spellings
        of the endpoint produce the same signature.
        """
        client = FuturesClient(secret=TEST_SECRET)
        with_prefix: str = client._get_kraken_futures_signature(
            endpoint="/derivatives/api/v3/sendorder",
            data="orderType=lmt&symbol=PI_XBTUSD",
            nonce="1616492376594",
        )
        without_prefix: str = client._get_kraken_futures_signature(
            endpoint="/api/v3/sendorder",
            data="orderType=lmt&symbol=PI_XBTUSD",
            nonce="1616492376594",
        )
        assert with_prefix == without_prefix

    def test_check_send_status_passes_clean_status(self: Self) -> None:
        """A non-error ``sendStatus`` is returned unchanged."""
        handler = ErrorHandler()
        data: dict = {"sendStatus": {"status": "placed"}}
        assert handler.check_send_status(data) == data

    def test_check_send_status_raises_on_error(self: Self) -> None:
        """A known error ``sendStatus`` raises the mapped Kraken exception."""
        handler = ErrorHandler()
        with pytest.raises(KrakenRequiredArgumentMissingError):
            handler.check_send_status(
                {"sendStatus": {"status": "requiredArgumentMissing"}},
            )

    def test_check_send_status_ignores_missing_key(self: Self) -> None:
        """A response without ``sendStatus`` is returned unchanged."""
        handler = ErrorHandler()
        data: dict = {"result": "success"}
        assert handler.check_send_status(data) == data

    def test_check_batch_status_passes_clean_batch(self: Self) -> None:
        """A batch where every status is clean is returned unchanged."""
        handler = ErrorHandler()
        data: dict = {"batchStatus": [{"status": "placed"}, {"status": "placed"}]}
        assert handler.check_batch_status(data) == data

    def test_check_batch_status_raises_on_error(self: Self) -> None:
        """A single error status within the batch raises the mapped exception."""
        handler = ErrorHandler()
        with pytest.raises(KrakenRequiredArgumentMissingError):
            handler.check_batch_status(
                {
                    "batchStatus": [
                        {"status": "placed"},
                        {"status": "requiredArgumentMissing"},
                    ],
                },
            )

    def test_get_nonce_is_increasing_numeric_string(self: Self) -> None:
        """The nonce is a numeric string that does not decrease over time."""
        client = FuturesClient()
        first: str = client.get_nonce()
        second: str = client.get_nonce()
        assert first.isdigit()
        assert second.isdigit()
        assert int(second) >= int(first)
