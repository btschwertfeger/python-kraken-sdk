#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module implementing the NFT Trade client"""

from __future__ import annotations

from typing import TypeVar

from kraken.base_api import NFTClient, defined

Self = TypeVar("Self")


class Trade(NFTClient):
    """
    Class that implements the Kraken NFT Trade client. Can be used to access
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
        :caption: NFT Trade: Create the Trade client

        >>> from kraken.nft import Trade
        >>> trade = Trade() # unauthenticated
        >>> auth_trade = Trade(key="api-key", secret="secret-key") # authenticated

    .. code-block:: python
        :linenos:
        :caption: NFT Trade:

        >>> from kraken.nft import Trade
        >>> with Trade(key="api-key", secret="secret-key") as trade:
        ...     print(trade.)
    """

    def __init__(
        self: Trade,
        key: str = "",
        secret: str = "",
        url: str = "",
        proxy: str | None = None,
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, proxy=proxy)

    def __enter__(self: Self) -> Self:
        super().__enter__()
        return self

    def create_auction(  # pylint: disable=too-many-arguments
        self: Trade,
        auction_currency: str,
        auction_params: dict,
        auction_type: str,
        nft_id: list[str],
        offer_id: str | None = None,
        otp: str | None = None,
        start_time: int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create an NFT auction for the user owned NFTs.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/createAuction

        :param auction_currency: The currency code
        :type auction_currency: str
        :param auction_params: Custom parameters set for this auction
        :type auction_params: dict
        :param auction_type: The type of auction
        :type auction_type: str
        :param nft_id: List of NFT IDs to put in auction
        :type nft_id: list[str]
        :param offer_id: Optional offer ID, defaults to None
        :type offer_id: Optional[str], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional
        :param start_time: Custom start time of that auction, defaults to None
        :type start_time: Optional[int], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Create Auction

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.create_auction(
            ...     auction_currency="ETH",
            ...     nft_id=["NT4EFBO-OWGI5-QLO7AG"],
            ...     auction_type="fixed",
            ...     auction_params={"allow_offers": True, "ask_price": 10},
            ... )
        """
        params: dict = {
            "auction_currency": auction_currency,
            "auction_params": auction_params,
            "auction_type": auction_type,
            "nft_id": nft_id,
        }
        if defined(offer_id):
            params["offer_id"] = offer_id
        if defined(otp):
            params["otp"] = otp
        if defined(start_time):
            params["start_time"] = start_time

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftCreateAuction",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )

    def modify_auction(
        self: Trade,
        auction_id: str,
        ask_price: str | int | None = None,
        otp: str | None = None,
        reserve_price: str | int | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Modify an existing auction owned by the user

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/modifyAuction

        :param auction_id: ID referencing the auction
        :type auction_id: str
        :param ask_price: New ask price (only for fixed price auction type),
            defaults to None
        :type ask_price: Optional[str | int], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional
        :param reserve_price: New reserve price (only for descending auction
            type), defaults to None
        :type reserve_price: Optional[str | int], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Create Auction

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.modify_auction(
            ...     auction_id="AT2POJ-4CH3O-4TH6JH",ask_price="0.3",
            ... )
        """
        params: dict = {"auction_id": auction_id}
        if defined(ask_price):
            params["ask_price"] = ask_price
        if defined(otp):
            params["otp"] = otp
        if defined(reserve_price):
            params["reserve_price"] = reserve_price

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftModifyAuction",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def cancel_auction(
        self: Trade,
        auction_ids: list[str],
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Cancel an existing auction owned by the user

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/cancelAuction

        :param auction_id: IDs referencing the auctions to cancel
        :type auction_id: list[str]
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Cancel Auction

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.cancel_auction(auction_ids=["AT2POJ-4CH3O-4TH6JH"])
        """
        params: dict = {"auction_ids": auction_ids}
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftCancelAuction",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )

    def place_offer(
        self: Trade,
        nft_id: list[str],
        offer_amount: str | int,
        offer_currency: str,
        quote_id: str | None = None,
        expire_time: int | None = None,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Place a new NFT offer.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/placeOffer

        :param nft_id: The NFT ID of interest
        :type nft_id: list[str]
        :param offer_amount: Offer amount
        :type offer_amount: str | int
        :param offer_currency: Offer Currency
        :type offer_currency: str
        :param quote_id: Quote ID, defaults to None
        :type quote_id: Optional[str], optional
        :param expire_time: Expire time of that offer, defaults to None
        :type expire_time: Optional[int], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Create Offer

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.place_offer(
            ...     nft_id=["AT2POJ-4CH3O-4TH6JH"],
            ...     offer_amount=1,
            ...     offer_currency="MATIC",
            ... )
        """
        params: dict = {
            "nft_id": nft_id,
            "offer_amount": offer_amount,
            "offer_currency": offer_currency,
        }
        if defined(quote_id):
            params["quote_id"] = quote_id
        if defined(expire_time):
            params["expire_time"] = expire_time
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftPlaceOffer",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )

    def counter_offer(
        self: Trade,
        currency: str,
        ask_price: str | int,
        offer_id: str,
        expire_time: int | None = None,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Create a counter offer for an existing offer.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/counterNftOffer

        :param currency: The currency to pay with
        :type currency: str
        :param ask_price: The counter offer ask price
        :type ask_price: str | int
        :param offer_id: The related offer ID
        :type offer_id: str
        :param expire_time: Expire time for that counter, defaults to None
        :type expire_time: Optional[int], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Create Counter Offer

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.counter_offer(
            ...    currency="MATIC",
            ...    ask_price=1,
            ...    offer_id="ONQYPLG-OFARL-35RBGO",
            ... )
        """
        params: dict = {
            "currency": currency,
            "ask_price": ask_price,
            "offer_id": offer_id,
        }
        if defined(expire_time):
            params["expire_time"] = expire_time
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftCounterOffer",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def accept_offer(
        self: Trade,
        offer_id: str,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Accept a specific NFT offer.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/acceptNftOffer

        :param offer_id: The related offer ID
        :type offer_id: str
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Create Counter Offer

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.accept_offer(offer_id="ONQYPLG-OFARL-35RBGO)
        """
        params: dict = {"offer_id": offer_id}
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftAcceptOffer",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def get_auction_trades(
        self: Trade,
        auction_id: list[str] | None = None,
        end_time: int | None = None,
        start_time: int | None = None,
        nft_id: str | None = None,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Get and filter for NFT auctions trades.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/getAuctionTrades

        :param auction_id: Auction ID to filter, defaults to None
        :type auction_id: Optional[list[str]], optional
        :param end_time: Filter end time, defaults to None
        :type end_time: Optional[int], optional
        :param start_time: Filter start time, defaults to None
        :type start_time: Optional[int], optional
        :param nft_id: NFT ID, defaults to None
        :type nft_id: Optional[str], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Get Auction trades

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.get_auction_trades()
        """
        params: dict = {}
        if defined(auction_id):
            params["auction_id"] = auction_id
        if defined(end_time):
            params["end_time"] = end_time
        if defined(start_time):
            params["start_time"] = start_time
        if defined(nft_id):
            params["nft_id"] = nft_id
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftAuctionTrades",
            params=params,
            auth=True,
            extra_params=extra_params,
        )

    def get_user_offers(  # noqa: PLR0913,PLR0917 # pylint: disable=too-many-arguments
        self: Trade,
        pos: int,
        scope: str,
        sort: str,
        chain: list[str] | None = None,
        collection: list[str] | None = None,
        count: int | None = None,
        end_time: int | None = None,
        start_time: int | None = None,
        exclude_quotes: bool | None = None,  # noqa: FBT001
        nft_id: str | None = None,
        status: str | None = None,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Retrieve and filter the user specific offers

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/getUserOffers

        :param pos: Paging offset
        :type pos: int
        :param scope: ``placed`` or ``received`` offers
        :type scope: str
        :param sort: ``asc`` or ``desc``
        :type sort: str
        :param chain: Filter by chain ID, defaults to None
        :type chain: Optional[list[str]], optional
        :param collection: Filter by collection, defaults to None
        :type collection: Optional[list[str]], optional
        :param count: Offers to return per request, defaults to None
        :type count: Optional[int], optional
        :param end_time: Latest offer time, defaults to None
        :type end_time: Optional[int], optional
        :param start_time: Oldest offer time, defaults to None
        :type start_time: Optional[int], optional
        :param exclude_quotes: Exclude quotes, defaults to None
        :type exclude_quotes: Optional[bool], optional
        :param nft_id: Filter by NFT ID, defaults to None
        :type nft_id: Optional[str], optional
        :param status: Filter by offer status, defaults to None
        :type status: Optional[str], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Get User Offers

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.get_user_offers(
            ...     pos=1,
            ...     scope="placed",
            ...     sort="asc",
            ...     chain=["MATIC"],
            ...     exclude_quotes=True,
            ...     status="open",
            ...     count=10,
            ...     collection=["NCQNABO-XYCA7-JMMSDF"],
            ... )
        """
        params: dict = {
            "pos": pos,
            "scope": scope,
            "sort": sort,
        }
        if defined(chain):
            params["chain"] = chain
        if defined(collection):
            params["collection"] = collection
        if defined(count):
            params["count"] = count
        if defined(end_time):
            params["end_time"] = end_time
        if defined(start_time):
            params["start_time"] = start_time
        if defined(exclude_quotes):
            params["exclude_quotes"] = exclude_quotes
        if defined(nft_id):
            params["nft_id"] = nft_id
        if defined(status):
            params["status"] = status
        if defined(otp):
            params["otp"] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftUserOffers",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )

    def get_nft_wallet(  # noqa: PLR0913,PLR0917,C901 # pylint: disable=too-many-arguments
        self: Trade,
        chain: str | None = None,
        currency: str | None = None,
        custody: str | None = None,
        page: int = 1,
        per_page: int = 5,
        price_currency: str | None = None,
        price_high: str | float | None = None,
        price_low: str | float | None = None,
        search: str | None = None,
        sort: str | None = None,
        status: list[str] | None = None,
        otp: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Filter for user owned NFT wallets.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/getNftWallet

        :param chain: Filter by chain, defaults to None
        :type chain: Optional[str], optional
        :param currency: Currency to show prices, defaults to None
        :type currency: Optional[str], optional
        :param custody: ``Kraken`` or ``Wallet``, defaults to None
        :type custody: Optional[str], optional
        :param page: Filter by page, defaults to 1
        :type page: int, optional
        :param per_page: Results per page, defaults to 5
        :type per_page: int, optional
        :param price_currency: Price currency, defaults to None
        :type price_currency: Optional[str], optional
        :param price_high: Price high, defaults to None
        :type price_high: Optional[str | float | int], optional
        :param price_low: Price low, defaults to None
        :type price_low: Optional[str | float | int], optional
        :param search: Filter by NFT title/description, defaults to None
        :type search: Optional[str], optional
        :param sort: Sort results, defaults to None
        :type sort: Optional[str], optional
        :param status: Filter by status, defaults to None
        :type status: Optional[list[str]], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: Get NFT Wallets

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.get_nft_wallet()
        """
        params: dict = {
            "page": page,
            "per_page": per_page,
        }
        if defined(chain):
            params[chain] = chain
        if defined(currency):
            params[currency] = currency
        if defined(custody):
            params[custody] = custody
        if defined(price_currency):
            params[price_currency] = price_currency
        if defined(price_high):
            params[price_high] = price_high
        if defined(price_low):
            params[price_low] = price_low
        if defined(search):
            params[search] = search
        if defined(sort):
            params[sort] = sort
        if defined(status):
            params[status] = status
        if defined(otp):
            params[otp] = otp

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftWallet",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )

    def list_nft_transactions(  # noqa: PLR0913 # pylint: disable=too-many-arguments
        self: Trade,
        end_time: int | None = None,
        start_time: int | None = None,
        nft_id: str | None = None,
        otp: str | None = None,
        page: int = 1,
        per_page: int = 5,
        sort: str = "desc",
        type_: str | None = None,
        *,
        extra_params: dict | None = None,
    ) -> dict:
        """
        Filter the users historical NFT transactions.

        - https://docs.kraken.com/rest/#tag/NFT-Trading/operation/listNftTransactions

        :param end_time: Latest result, defaults to None
        :type end_time: Optional[int], optional
        :param start_time: Oldest result, defaults to None
        :type start_time: Optional[int], optional
        :param nft_id: Filter by NFT ID, defaults to None
        :type nft_id: Optional[str], optional
        :param otp: One time password, defaults to None
        :type otp: Optional[str], optional
        :param page: Start page, defaults to 1
        :type page: int, optional
        :param per_page: Entries per page, defaults to 5
        :type per_page: int, optional
        :param sort: Sort results by, defaults to "desc"
        :type sort: str, optional
        :param type_: Transaction type, defaults to None
        :type type_: Optional[str], optional

        .. code-block:: python
            :linenos:
            :caption: NFT Trade: List NFT Transactions

            >>> from kraken.nft import Trade
            >>> trade = Trade()
            >>> trade.list_nft_transactions()

        """
        params: dict = {
            "page": page,
            "per_page": per_page,
            "sort": sort,
        }
        if defined(end_time):
            params[end_time] = end_time
        if defined(start_time):
            params[start_time] = start_time
        if defined(nft_id):
            params[nft_id] = nft_id
        if defined(otp):
            params[otp] = otp
        if defined(type_):
            params[type_] = type_

        return self.request(  # type: ignore[return-value]
            method="POST",
            uri="/0/private/NftTransactions",
            params=params,
            auth=True,
            do_json=True,
            extra_params=extra_params,
        )
