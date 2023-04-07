#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger


"""Module that provides custom exceptions for the python-kraken-sdk"""
import functools
from typing import List


class KrakenException:
    """
    Class that provides custom exceptions for the python-kraken-sdk based on the
    error messages that can be received from the Kraken Spot and Futures API.

    - https://docs.kraken.com/rest/#section/General-Usage/Requests-Responses-and-Errors
    """

    def __init__(self, msg=None, *args, **kwargs):
        self.EXCEPTION_ASSIGNMENT = {
            ##      Spot, Margin, and Futures trading Errors
            ##
            "EGeneral:Invalid arguments": self.KrakenInvalidArgumentsError,
            "EGeneral:Invalid arguments:Index unavailable": self.KrakenInvalidArgumentsIndexUnavailableError,
            "EGeneral:Permission denied": self.KrakenPermissionDeniedError,
            "EService:Unavailable": self.KrakenServiceUnavailableError,
            "EService:Market in cancel_only mode": self.KrakenMarketInOnlyCancelModeError,
            "EService:Market in post_only mode": self.KrakenMarketInOnlyPostModeError,
            "EService:Deadline elapsed": self.KrakenDeadlineElapsedError,
            "EAPI:Invalid key": self.KrakenInvalidAPIKeyError,
            "EAPI:Invalid signature": self.KrakenInvalidSignatureError,
            "EAPI:Invalid nonce": self.KrakenInvalidNonceError,
            "EOrder:Invalid order": self.KrakenInvalidOrderError,
            "EOrder:Invalid price": self.KrakenInvalidPriceError,
            "EOrder:Cannot open position": self.KrakenCannotOpenPositionError,
            "EOrder:Margin allowance exceeded": self.KrakenMarginAllowedExceededError,
            "EOrder:Margin level too low": self.KrakenMarginLevelToLowError,
            "EOrder:Margin position size exceeded": self.KrakenMarginPositionSizeExceededError,
            "EOrder:Insufficient margin": self.KrakenInsufficientMarginError,
            "EOrder:Insufficient funds": self.KrakenInsufficientFundsError,
            "EOrder:Order minimum not met": self.KrakenOrderMinimumNotMetError,
            "EOrder:Cost minimum not met": self.KrakenCostMinimumNotMetError,
            "EOrder:Tick size check failed": self.KrakenTickSizeInvalidCheckError,
            "EOrder:Orders limit exceeded": self.KrakenOrderLimitsExceededError,
            "EOrder:Rate limit exceeded": self.KrakenRateLimitExceededError,
            "EOrder:Positions limit exceeded": self.KrakenPositionLimitExceeded,
            "EOrder:Unknown order": self.KrakenUnknownOrderError,
            "EOrder:Unknown position": self.KrakenUnknownPositionError,
            "EFunding:Invalid reference id": self.KrakenInvalidReferenceIdError,
            "EFunding:Unknown reference id": self.KrakenUnknownReferenceIdError,
            "EFunding:Unknown withdraw key": self.KrakenUnknownWithdrawKeyError,
            "EFunding:Invalid amount": self.KrakenInvalidAmountError,
            "EFunding:Invalid staking method": self.KrakenInvalidStakingMethodError,
            "EFunding:Too many addresses": self.KrakenToManyAdressesError,
            "EFunding:Unknown asset": self.KrakenUnknownAssetError,
            "EQuery:Unknown asset": self.KrakenUnknownAssetError,
            "EQuery:Unknown asset pair": self.KrakenUnknownAssetPairError,
            ##      Futures Trading Errors
            ##
            "authenticationError": self.KrakenAuthenticationError,
            "insufficientAvailableFunds": self.KrakenInsufficientAvailableFundsError,
            "apiLimitExceeded": self.KrakenApiLimitExceededError,
            "invalidUnit": self.KrakenInvalidUnitError,
            "Unavailable": self.KrakenUnavailableError,
            "invalidAccount": self.KrakenInvalidAccountError,
            "notFound": self.KrakenNotFoundError,
            "orderForEditNotFound": self.KrakenOrderForEditNotFoundError,
        }

    def get_exception(self, data: List[str]):
        """Returns the exception given by name if available"""
        is_list = isinstance(data, list)
        for name, exception in self.EXCEPTION_ASSIGNMENT.items():
            if is_list:
                if name in data:
                    return exception
                for err in data:
                    if name in err:
                        return exception
            elif data == name:
                return exception
        return None

    def docstring_message(cls):
        """Decorates an exception to make its docstring its default message.
        https://stackoverflow.com/a/66491013/13618168
        """
        cls_init = cls.__init__

        @functools.wraps(cls.__init__)
        def wrapped_init(self, msg=None, *args, **kwargs):
            err_message = self.__doc__ if not msg else f"{self.__doc__}\ndetails: {msg}"
            cls_init(self, err_message, *args, **kwargs)

        cls.__init__ = wrapped_init
        return cls

    @docstring_message
    class KrakenInvalidArgumentsError(Exception):
        """The request payload is malformed, incorrect or ambiguous."""

    @docstring_message
    class KrakenInvalidArgumentsIndexUnavailableError(Exception):
        """Index pricing is unavailable for stop/profit orders on this pair."""

    @docstring_message
    class KrakenPermissionDeniedError(Exception):
        """API key doesn't have permission to make this request."""

    @docstring_message
    class KrakenServiceUnavailableError(Exception):
        """The matching engine or API is offline."""

    @docstring_message
    class KrakenMarketInOnlyCancelModeError(Exception):
        """Request can't be made at this time. Please check system status."""

    @docstring_message
    class KrakenMarketInOnlyPostModeError(Exception):
        """Request can't be made at this time. Please check system status."""

    @docstring_message
    class KrakenDeadlineElapsedError(Exception):
        """The request timed out according to the default or specified deadline."""

    @docstring_message
    class KrakenInvalidAPIKeyError(Exception):
        """An invalid API-Key header was supplied."""

    @docstring_message
    class KrakenInvalidSignatureError(Exception):
        """An invalid API-Sign header was supplied."""

    @docstring_message
    class KrakenInvalidNonceError(Exception):
        """An invalid nonce was supplied."""

    @docstring_message
    class KrakenInvalidOrderError(Exception):
        """Order is invalid."""

    @docstring_message
    class KrakenInvalidPriceError(Exception):
        """Price is invalid."""

    @docstring_message
    class KrakenAuthenticationError(Exception):
        """Credentials are invalid."""

    @docstring_message
    class KrakenCannotOpenPositionError(Exception):
        """User/tier is ineligible for margin trading."""

    @docstring_message
    class KrakenMarginAllowedExceededError(Exception):
        """User has exceeded their margin allowance."""

    @docstring_message
    class KrakenMarginLevelToLowError(Exception):
        """Client has insufficient equity or collateral."""

    @docstring_message
    class KrakenMarginPositionSizeExceededError(Exception):
        """Client would exceed the maximum position size for this pair."""

    @docstring_message
    class KrakenInsufficientMarginError(Exception):
        """Exchange does not have available funds for this margin trade."""

    @docstring_message
    class KrakenInsufficientFundsError(Exception):
        """Client does not have the necessary funds."""

    @docstring_message
    class KrakenInsufficientAvailableFundsError(Exception):
        """Client does not have the necessary funds."""

    @docstring_message
    class KrakenOrderMinimumNotMetError(Exception):
        """Order size does not meet ordermin."""

    @docstring_message
    class KrakenCostMinimumNotMetError(Exception):
        """Cost (price * volume) does not meet costmin."""

    @docstring_message
    class KrakenTickSizeInvalidCheckError(Exception):
        """Price submitted is not a valid multiple of the pair's tick_size."""

    @docstring_message
    class KrakenOrderLimitsExceededError(Exception):
        """Order limits exceeded. Please check your open orders limit."""

    @docstring_message
    class KrakenRateLimitExceededError(Exception):
        """API rate limit exceeded. Please check your rate limits."""

    @docstring_message
    class KrakenApiLimitExceededError(Exception):
        """API rate limit exceeded. Please check your rate limits."""

    @docstring_message
    class KrakenPositionLimitExceeded(Exception):
        """Position limit exceeded. Please check your limits."""

    @docstring_message
    class KrakenUnknownOrderError(Exception):
        """Order is unknown."""

    @docstring_message
    class KrakenUnknownPositionError(Exception):
        """Position is unknown."""

    @docstring_message
    class KrakenUnknownAssetPairError(Exception):
        """The asset pair is unknown."""

    @docstring_message
    class KrakenUnknownAssetError(Exception):
        """The asset is unknown."""

    @docstring_message
    class KrakenInvalidUnitError(Exception):
        """The specified unit is invalid."""

    @docstring_message
    class KrakenUnavailableError(Exception):
        """The requested resource is unavailable."""

    @docstring_message
    class KrakenInvalidReferenceIdError(Exception):
        """The requested referece id is invalid."""

    @docstring_message
    class KrakenUnknownReferenceIdError(Exception):
        """The requested referece id is unknown."""

    @docstring_message
    class KrakenUnknownWithdrawKeyError(Exception):
        """The requested withdrawal key is unknown."""

    @docstring_message
    class KrakenInvalidAmountError(Exception):
        """The specified amount is invalid."""

    @docstring_message
    class KrakenInvalidStakingMethodError(Exception):
        """The staking method is invalid."""

    @docstring_message
    class KrakenInvalidAccountError(Exception):
        """The account is invalid."""

    @docstring_message
    class KrakenNotFoundError(Exception):
        """The resource is not found."""

    @docstring_message
    class KrakenOrderForEditNotFoundError(Exception):
        """The order for edit could not be found."""

    @docstring_message
    class KrakenToManyAdressesError(Exception):
        """To many adresses specified."""

    # ? ____CUSTOM_EXCEPTIONS_________
    @docstring_message
    class MaxReconnectError(Exception):
        """To many reconnect tries."""
