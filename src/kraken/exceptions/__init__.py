# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that provides custom exceptions for the python-kraken-sdk"""

from __future__ import annotations

import functools
from typing import Any, TypeVar

Self = TypeVar("Self")


def docstring_message(cls: Any) -> Any:  # noqa: ANN401
    """
    Decorates an exception to make its docstring its default message.

    - https://stackoverflow.com/a/66491013/13618168
    """
    cls_init = cls.__init__

    @functools.wraps(cls.__init__)
    def wrapped_init(
        self: Self,
        msg: str | dict | None = None,
        *args: tuple,
        **kwargs: dict[str, Any],
    ) -> None:
        err_message: str = (
            self.__doc__ if not msg else f"{self.__doc__}\nDetails: {msg}"
        )
        cls_init(self, err_message, *args, **kwargs)

    cls.__init__ = wrapped_init
    return cls


@docstring_message
class KrakenInvalidArgumentsError(Exception):
    """The request payload is malformed, incorrect or ambiguous."""


@docstring_message
class KrakenBadRequestError(Exception):
    """The request payload is malformed, incorrect or ambiguous."""


@docstring_message
class KrakenRequiredArgumentMissingError(Exception):
    """The request is missing a required argument."""


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
class KrakenAuthenticationFailedError(Exception):
    """The account or its permissions could not be authenticated."""


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
class KrakenPositionLimitExceededError(Exception):
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
    """The requested reference id is invalid."""


@docstring_message
class KrakenUnknownReferenceIdError(Exception):
    """The requested reference id is unknown."""


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
class KrakenToManyAddressesError(Exception):
    """To many addresses specified."""


@docstring_message
class KrakenUnknownMethodError(Exception):
    """The endpoint or method is not known."""


@docstring_message
class KrakenTemporaryLockoutError(Exception):
    """The account was temporary locked out."""


@docstring_message
class KrakenEarnMinimumAllocationError(Exception):
    """(De)allocation operation amount less than minimum"""


@docstring_message
class KrakenEarnAllocationInProgressError(Exception):
    """Another allocation is already in progress"""


@docstring_message
class KrakenEarnTemporaryUnavailableError(Exception):
    """The Earn service is temporary unavailable, try again in a few minutes"""


@docstring_message
class KrakenEarnTierVerificationError(Exception):
    """The user's tier is not high enough"""


@docstring_message
class KrakenEarnStrategyNotFoundError(Exception):
    """Strategy not found"""


@docstring_message
class KrakenEarnInsufficientFundsError(Exception):
    """Insufficient funds to complete the transaction"""


@docstring_message
class KrakenEarnAllocationExceededError(Exception):
    """The allocation exceeds user limit for the strategy"""


@docstring_message
class KrakenEarnDeallocationExceededError(Exception):
    """The deallocation exceeds user limit for the strategy"""


@docstring_message
class KrakenMaxFeeExceededError(Exception):
    """The fee was higher than the defined maximum."""


@docstring_message
class KrakenNFTNotAvailableError(Exception):
    """The user doesn't own the selected NFT."""


@docstring_message
class KrakenInvalidArgumentsStartTimeError(Exception):
    """start_time must be < expire_time"""


@docstring_message
class KrakenInvalidArgumentsExpireTimeError(Exception):
    """expire_time above max"""


@docstring_message
class KrakenAuctionNotOwnedByUserError(Exception):
    """The Auction is not owned by the current user."""


@docstring_message
class KrakenInvalidArgumentBelowMinError(Exception):
    """The defined price is lower than the required minimum."""


@docstring_message
class KrakenInvalidArgumentOfferNotFoundError(Exception):
    """The requested offer was not found."""


@docstring_message
class MaxReconnectError(Exception):
    """To many reconnect tries."""


EXCEPTION_ASSIGNMENT: dict[str, Any] = {
    #      Spot, Margin, and Futures trading Errors
    #
    "EGeneral:Invalid arguments": KrakenInvalidArgumentsError,
    "EGeneral:Invalid arguments:Index unavailable": KrakenInvalidArgumentsIndexUnavailableError,
    "EGeneral:Permission denied": KrakenPermissionDeniedError,
    "EGeneral:Unknown method": KrakenUnknownMethodError,
    "EGeneral:Temporary lockout": KrakenTemporaryLockoutError,
    "EGeneral:No Balance:nfts not available": KrakenNFTNotAvailableError,
    "EGeneral:Invalid User:auction owned by someone else": KrakenAuctionNotOwnedByUserError,
    "EFunding:Max fee exceeded": KrakenMaxFeeExceededError,
    "EService:Unavailable": KrakenServiceUnavailableError,
    "EService:Market in cancel_only mode": KrakenMarketInOnlyCancelModeError,
    "EService:Market in post_only mode": KrakenMarketInOnlyPostModeError,
    "EService:Deadline elapsed": KrakenDeadlineElapsedError,
    "EAuth:Failed": KrakenAuthenticationFailedError,
    "EAPI:Invalid key": KrakenInvalidAPIKeyError,
    "EAPI:Invalid signature": KrakenInvalidSignatureError,
    "EAPI:Invalid nonce": KrakenInvalidNonceError,
    "EAPI:Invalid arguments:start_time must be < expire_time": KrakenInvalidArgumentsStartTimeError,
    "EAPI:Invalid arguments:expire_time above max": KrakenInvalidArgumentsExpireTimeError,
    "EAPI:Invalid arguments:price below min": KrakenInvalidArgumentBelowMinError,
    "EAPI:Invalid arguments:offer not found": KrakenInvalidArgumentOfferNotFoundError,
    "EAPI:Rate limit exceeded": KrakenApiLimitExceededError,
    "EAPI:Bad request": KrakenBadRequestError,
    "EOrder:Invalid order": KrakenInvalidOrderError,
    "EOrder:Invalid price": KrakenInvalidPriceError,
    "EOrder:Cannot open position": KrakenCannotOpenPositionError,
    "EOrder:Margin allowance exceeded": KrakenMarginAllowedExceededError,
    "EOrder:Margin level too low": KrakenMarginLevelToLowError,
    "EOrder:Margin position size exceeded": KrakenMarginPositionSizeExceededError,
    "EOrder:Insufficient margin": KrakenInsufficientMarginError,
    "EOrder:Insufficient funds": KrakenInsufficientFundsError,
    "EOrder:Order minimum not met": KrakenOrderMinimumNotMetError,
    "EOrder:Cost minimum not met": KrakenCostMinimumNotMetError,
    "EOrder:Tick size check failed": KrakenTickSizeInvalidCheckError,
    "EOrder:Orders limit exceeded": KrakenOrderLimitsExceededError,
    "EOrder:Rate limit exceeded": KrakenRateLimitExceededError,
    "EOrder:Positions limit exceeded": KrakenPositionLimitExceededError,
    "EOrder:Unknown order": KrakenUnknownOrderError,
    "EOrder:Unknown position": KrakenUnknownPositionError,
    "EFunding:Invalid reference id": KrakenInvalidReferenceIdError,
    "EFunding:Unknown reference id": KrakenUnknownReferenceIdError,
    "EFunding:Unknown withdraw key": KrakenUnknownWithdrawKeyError,
    "EFunding:Invalid amount": KrakenInvalidAmountError,
    "EFunding:Invalid staking method": KrakenInvalidStakingMethodError,
    "EFunding:Too many addresses": KrakenToManyAddressesError,
    "EFunding:Unknown asset": KrakenUnknownAssetError,
    "EQuery:Unknown asset": KrakenUnknownAssetError,
    "EQuery:Unknown asset pair": KrakenUnknownAssetPairError,
    # "WDatabase:No change": ,
    #      Futures Trading Errors
    #
    "EEarnings:Below min:(De)allocation operation amount less than minimum": KrakenEarnMinimumAllocationError,
    "EEarnings:Busy:Another (de)allocation for the same strategy is in progress": KrakenEarnAllocationInProgressError,
    "EEarnings:Busy": KrakenEarnTemporaryUnavailableError,
    "EEarnings:Permission denied:The user's tier is not high enough": KrakenEarnTierVerificationError,
    "EGeneral:Invalid arguments:Invalid strategy ID": KrakenEarnStrategyNotFoundError,
    "EEarnings:Insufficient funds:Insufficient funds to complete the (de)allocation request": KrakenEarnInsufficientFundsError,
    "EEarnings:Above max:The allocation exceeds user limit for the strategy": KrakenEarnAllocationExceededError,
    "EEarnings:Above max:The allocation exceeds the total strategy limit": KrakenEarnDeallocationExceededError,
    "authenticationError": KrakenAuthenticationError,
    "insufficientAvailableFunds": KrakenInsufficientAvailableFundsError,
    "requiredArgumentMissing": KrakenRequiredArgumentMissingError,
    "apiLimitExceeded": KrakenApiLimitExceededError,
    "invalidUnit": KrakenInvalidUnitError,
    "Unavailable": KrakenUnavailableError,
    "invalidAccount": KrakenInvalidAccountError,
    "notFound": KrakenNotFoundError,
    "orderForEditNotFound": KrakenOrderForEditNotFoundError,
}


def _get_exception(data: str | list[str]) -> Any | None:  # noqa: ANN401
    """Returns the exception given by name if available"""
    is_list: bool = isinstance(data, list)
    for name, exception in EXCEPTION_ASSIGNMENT.items():
        if is_list:
            if name in data:
                return exception
            for err in data:
                if name in err:
                    return exception
        elif data == name:
            return exception
    return None


__all__ = [
    "KrakenApiLimitExceededError",
    "KrakenAuthenticationError",
    "KrakenAuthenticationFailedError",
    "KrakenBadRequestError",
    "KrakenCannotOpenPositionError",
    "KrakenCostMinimumNotMetError",
    "KrakenDeadlineElapsedError",
    "KrakenInsufficientAvailableFundsError",
    "KrakenInsufficientFundsError",
    "KrakenInsufficientMarginError",
    "KrakenInvalidAccountError",
    "KrakenInvalidAmountError",
    "KrakenInvalidAPIKeyError",
    "KrakenInvalidArgumentsError",
    "KrakenInvalidArgumentsIndexUnavailableError",
    "KrakenInvalidNonceError",
    "KrakenInvalidOrderError",
    "KrakenInvalidPriceError",
    "KrakenInvalidReferenceIdError",
    "KrakenInvalidSignatureError",
    "KrakenInvalidStakingMethodError",
    "KrakenInvalidUnitError",
    "KrakenMarginAllowedExceededError",
    "KrakenMarginLevelToLowError",
    "KrakenMarginPositionSizeExceededError",
    "KrakenMarketInOnlyCancelModeError",
    "KrakenMarketInOnlyPostModeError",
    "KrakenMaxFeeExceededError",
    "KrakenNotFoundError",
    "KrakenOrderForEditNotFoundError",
    "KrakenOrderLimitsExceededError",
    "KrakenOrderMinimumNotMetError",
    "KrakenPermissionDeniedError",
    "KrakenPositionLimitExceededError",
    "KrakenRateLimitExceededError",
    "KrakenRequiredArgumentMissingError",
    "KrakenServiceUnavailableError",
    "KrakenTemporaryLockoutError",
    "KrakenTickSizeInvalidCheckError",
    "KrakenToManyAddressesError",
    "KrakenUnavailableError",
    "KrakenUnknownAssetError",
    "KrakenUnknownAssetPairError",
    "KrakenUnknownMethodError",
    "KrakenUnknownOrderError",
    "KrakenUnknownPositionError",
    "KrakenUnknownReferenceIdError",
    "KrakenUnknownWithdrawKeyError",
    "MaxReconnectError",
]
