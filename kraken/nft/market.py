#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that implements the Kraken Futures market client"""

from __future__ import annotations

from typing import Optional, TypeVar

from kraken.base_api import KrakenNFTBaseAPI, defined

Self = TypeVar("Self")


class Market(KrakenNFTBaseAPI):
    """
    Class that implements the Kraken NFT Market client. Can be used to access
    the Kraken NFT market data.

    :param key: Spot API public key (default: ``""``)
    :type key: str, optional
    :param secret: Spot API secret key (default: ``""``)
    :type secret: str, optional

    .. code-block:: python
        :linenos:
        :caption: NFT Market: Create the market client

        >>> from kraken.nft import Market
        >>> market = Market() # unauthenticated
        >>> auth_market = Market(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: NFT Market: Create the market client as context manager

        >>> from kraken.nft import Market
        >>> with Market() as market:
        ...     print(market.get_assets())
    """

    def __init__(
        self: Market,
        key: str = "",
        secret: str = "",
        url: str = "",
    ) -> None:
        super().__init__(key=key, secret=secret, url=url)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def get_nft(
        self: Market,
        nft_id: str,
        currency: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Get an NFT by ID

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getNft

        :param nft_id: The ID of the NFT
        :type nft_id: str
        :param currency: Fiat currency for representing prices, defaults to None
        :type currency: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get a specific NFT

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_nft(nft_id="NT4GUCU-SIJE2-YSQQG2")
            {
                "nft": {
                    "id": "NT4GUCU-SIJE2-YSQQG2",
                    "name": "#3210 Williams Racing Collectibles+ Grid Pass",
                    "description": "Grants access to a community of Williams Racing super-fans.",
                    "max_count": 1,
                    "external_url": None,
                    "image": {
                        "kind": "Main",
                        "media": {
                            "url": "https://assets-dynamic.kraken.com/media1/40c8fa182f98e6e77072df3ac8fe053e9e2ff064f3f0a470346bb7de0613c762.png",
                            "media_type": "image/png",
                            "size": 4334294
                        }
                    },
                    "media": [...],
                    ...
                },
                ...
            }
        """
        params: dict = {"nft_id": nft_id}
        if defined(currency):
            params["currency"] = currency
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Nft",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def list_nfts(
        self: Market,
        page_size: int,
        cursor: Optional[str] = None,
        filter_: Optional[str] = None,
        sort: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Filter the database for NFTs.

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/listNfts

        :param page_size: Number of items on a single page
        :type page_size: int
        :param cursor: Cursor token retrieved by a previous request, defaults to None
        :type cursor: Optional[str], optional
        :param filter: Filter by NFT attributes, defaults to None
        :type filter: Optional[str], optional
        :param sort: Sort the results, defaults to None
        :type sort: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: List and filter available NFTs

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.list_nfts(
            ...     page_size=1,
            ...     filter_="filter%5Bcollection_id%5D%3DNCQNABO-XYCA7-JMMSDF"
            ... )
        """
        params: dict = {"page_size": page_size}
        if defined(cursor):
            params["cursor"] = cursor
        if defined(sort):
            params["sort"] = sort

        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Nfts",
            params=params,
            query_str=filter_,
            auth=False,
            extra_params=extra_params,
        )

    def get_nft_provenance(
        self: Market,
        nft_id: str,
        page: int = 1,
        per_page: int = 5,
        currency: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Retrieve the historical ownership of an NFT

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getNftProvenance

        :param nft_id: The NFT ID
        :type nft_id: str
        :param page: Start page, defaults to 1
        :type page: int, optional
        :param per_page: Items per page, defaults to 5
        :type per_page: int, optional
        :param currency: The currency used for displaying values, defaults to
            None
        :type currency: str, optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get historical NFT ownership

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.list_nfts(
            ...     nft_id="NT4GUCU-SIJE2-YSQQG2",
            ... )
        """
        params: dict = {
            "nft_id": nft_id,
            "page": page,
            "per_page": per_page,
        }
        if defined(currency):
            params["currency"] = currency
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftProvenance",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_collection(
        self: Market,
        collection_id: str,
        currency: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        Get an NFT collection by ID

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getCollection

        :param collection_id: The Collection ID
        :type collection_id: str
        :param currency: Fiat currency to display values, defaults to None
        :type currency: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get NFT Collection

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_collection(
            ...     collection_id="NCQNABO-XYCA7-JMMSDF", currency="USD"
            ... )
        """
        params: dict = {"collection_id": collection_id}

        if defined(currency):
            params["currency"] = currency
        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCollection",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def list_collections(
        self: Market,
        page_size: int,
        currency: Optional[str] = None,
        cursor: Optional[str] = None,
        filter_: Optional[str] = None,
        sort: Optional[str] = None,
        *,
        extra_params: Optional[dict] = None,
    ) -> dict:
        """
        List available NFT collections

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/listCollections

        :param page_size: Page size
        :type page_size: int
        :param currency: Fiat currency to display values, defaults to None
        :type currency: Optional[str], optional
        :param cursor: Cursor token received by last request, defaults to None
        :type cursor: Optional[str], optional
        :param filter_: Apply filter, defaults to None
        :type filter_: Optional[str], optional
        :param sort: Define sorting, defaults to None
        :type sort: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: List NFT Collections

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.list_collections(
            ...         page_size=1,
            ...         currency="USD",
            ...         filter_="filter%5Bsearch%5D=Williams",
            ...         sort="MostRelevant",
            ... )
        """
        params: dict = {"page_size": page_size}
        if defined(currency):
            params["currency"] = currency
        if defined(cursor):
            params["cursor"] = cursor
        if defined(sort):
            params["sort"] = sort

        return self._request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCollections",
            params=params,
            query_str=filter_,
            auth=False,
            extra_params=extra_params,
        )
