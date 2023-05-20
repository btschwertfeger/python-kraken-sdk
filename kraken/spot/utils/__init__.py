#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger

"""Module that provides the Utils class that stores Spot related functions."""

from decimal import Decimal
from functools import lru_cache
from math import floor
from typing import Union

from ..market import Market


class Utils:
    """
    The Utils class provides utility functions for the Spot related clients.
    """

    @staticmethod
    @lru_cache()
    def truncate(
        amount: Union[Decimal, float, int, str], amount_type: str, pair: str
    ) -> str:
        """
        Kraken only allows volume and price amounts to be specified with a specific number of
        decimal places, and these varry depending on the currency pair used.

        This function converts an amount of a specific type and pair to a string that uses
        the correct number of decimal places.

        - https://support.kraken.com/hc/en-us/articles/4521313131540

        This function uses caching. Run ``Utils.truncate.clear_cache()`` to clear
        the cache.

        :param amount: The floating point number to represent
        :type amount: Decimal | float | int | str
        :param amount_type: What the amount represents. Either 'price' or 'volume'
        :type amount_type: str
        :param pair: The currency pair the amount is in reference to.
        :type pair: str
        :raises ValueError: If the ``amount_type`` is ``price`` and the price is less
            than the costmin.
        :raises ValueError: If the ``amount_type`` is ``volume`` and the volume is
            less than the ordermin.
        :raises ValueError: If no valid ``amount_type`` was passed.
        :return: A string representation of the amount.
        :rtype: str
        """
        if amount_type not in ("price", "volume"):
            raise ValueError("Amount type must be 'volume' or 'price'!")

        pair_data: dict = Market().get_asset_pairs(pair=pair)
        data: dict = pair_data[list(pair_data)[0]]

        pair_decimals: int = int(data["pair_decimals"])
        lot_decimals: int = int(data["lot_decimals"])

        ordermin: Decimal = Decimal(data["ordermin"])
        costmin: Decimal = Decimal(data["costmin"])

        amount = Decimal(amount)
        decimals: int

        if amount_type == "price":
            if costmin > amount:
                raise ValueError(f"Price is less than the costmin: {costmin}!")
            decimals = pair_decimals
        else:  # amount_type == "volume":
            if ordermin > amount:
                raise ValueError(f"Volume is less than the ordermin: {ordermin}!")
            decimals = lot_decimals

        amount_rounded: float = floor(float(amount) * 10**decimals) / 10**decimals
        return f"{amount_rounded:.{decimals}f}"
