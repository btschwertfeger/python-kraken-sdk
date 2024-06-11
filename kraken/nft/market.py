#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that implements the Kraken Futures market client"""

from __future__ import annotations

from typing import TypeVar

from kraken.base_api import NFTClient, defined

Self = TypeVar("Self")


class Market(NFTClient):
    """
    Class that implements the Kraken NFT Market client. Can be used to access
    the Kraken NFT market data.

    Please note that these API endpoints are new and still under development at
    Kraken. So the behavior and parameters may change unexpectedly. Please open
    an issue at https://github.com/btschwertfeger/python-kraken-sdk for any
    issues that can be addressed within this package.

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
        :caption: NFT Market: List Blockchains

        >>> from kraken.nft import Market
        >>> with Market() as market:
        ...     print(market.list_blockchains())
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
        currency: str | None = None,
        *,
        extra_params: dict | None = None,
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
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/Nft",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def list_nfts(
        self: Market,
        page_size: int,
        cursor: str | None = None,
        filter_: str | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
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
            ...     filter_="filter[collection_id]=NCQNABO-XYCA7-JMMSDF"
            ... )
        """
        params: dict = {"page_size": page_size}
        if defined(cursor):
            params["cursor"] = cursor
        if defined(sort):
            params["sort"] = sort

        return self.request(  # type: ignore[return-value]
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
        currency: str | None = None,
        *,
        extra_params: dict | None = None,
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
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftProvenance",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def get_collection(
        self: Market,
        collection_id: str,
        currency: str | None = None,
        *,
        extra_params: dict | None = None,
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
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCollection",
            params=params,
            auth=False,
            extra_params=extra_params,
        )

    def list_collections(
        self: Market,
        page_size: int,
        currency: str | None = None,
        cursor: str | None = None,
        filter_: str | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
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
            ...         filter_="filter[search]=Williams",
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

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCollections",
            params=params,
            query_str=filter_,
            auth=False,
            extra_params=extra_params,
        )

    def get_creator(
        self: Market,
        creator_id: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve information about a specific NFT creator

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getCreator

        :param creator_id: The ID of the creator
        :type creator_id: str

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get Creator

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_creator(creator_id="NA7NELE-FOQFZ-ODWOTV")
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCreator",
            params={"creator_id": creator_id},
            auth=False,
            extra_params=extra_params,
        )

    def list_creators(
        self: Market,
        page_size: int,
        currency: str | None = None,
        cursor: str | None = None,
        filter_: str | None = None,
        sort: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List and filter for NFT creators

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/listCreators

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
            :caption: NFT Market: Get Creators

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.list_creators(
            ...         page_size=1,
            ...         currency="USD",
            ...         filter_="filter[collection_search]=Williams",
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

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftCreators",
            params=params,
            query_str=filter_,
            auth=False,
            extra_params=extra_params,
        )

    def list_blockchains(
        self: Market,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the available blockchains

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/listBlockchains

        .. code-block:: python
            :linenos:
            :caption: NFT Market: List Blockchains

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.list_blockchains()
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftBlockchains",
            auth=False,
            extra_params=extra_params,
        )

    def get_auctions(
        self: Market,
        status: str,
        filter_: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the available NFT auctions

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getAuctions

        :param status: The current status of the auction
        :type status: str
        :param filter_: Filter for auctions
        :type filter_: str, optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get Auctions

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_auctions(
            ...     status="open"
            ...     filter_="nft_id[]=NTN63WS-PBAV3-FQDQDG"
            ... )
        """
        params: dict = {}
        if defined(status):
            params["status"] = status
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftAuctions",
            params=params,
            query_str=filter_,
            auth=False,
            extra_params=extra_params,
        )

    def get_offers(
        self: Market,
        nft_id: str,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the available NFT offers

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getOffers

        :param nft_id: The ID of the NFT
        :type nft_id: str

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get Offers

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_offers(nft_id="NT4GUCU-SIJE2-YSQQG2")
        """
        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftOffers",
            params={"nft_id": nft_id},
            auth=False,
            extra_params=extra_params,
        )

    def get_nft_quotes(
        self: Market,
        filter_: str,
        count: int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        List the available NFT quotes

        - https://docs.kraken.com/rest/#tag/NFT-Market-Data/operation/getNftQuotes

        :param filter: Apply specific filters
        :type filter: str
        :param count: Number of items to return
        :type count: int, optional

        .. code-block:: python
            :linenos:
            :caption: NFT Market: Get Quotes

            >>> from kraken.nft import Market
            >>> market = Market()
            >>> market.get_nft_quotes(
            ...     filter_="nft_id[]=NT4GUCU-SIJE2-YSQQG2",
            ...     count=2
            ... )
        """
        params: dict = {}
        if defined(count):
            params["count"] = count

        return self.request(  # type: ignore[return-value]
            method="GET",
            uri="/0/public/NftQuotes",
            query_str=filter_,
            params=params,
            auth=False,
            extra_params=extra_params,
        )
