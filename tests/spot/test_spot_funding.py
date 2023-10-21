#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot funding client."""

import pytest

from kraken.exceptions import KrakenInvalidArgumentsError, KrakenPermissionDeniedError
from kraken.spot import Funding

from .helper import is_not_error

# todo: Mock skipped tests - or is this to dangerous?


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
def test_get_deposit_methods(spot_auth_funding: Funding) -> None:
    """
    Checks if the response of the ``get_deposit_methods`` is of
    type list which mean that the request was successful.
    """
    assert isinstance(spot_auth_funding.get_deposit_methods(asset="XBT"), list)


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
def test_get_deposit_address(spot_auth_funding: Funding) -> None:
    """
    Checks the ``get_deposit_address`` function by performing a valid request
    and validating that the response is of type list.
    """
    assert isinstance(
        spot_auth_funding.get_deposit_address(asset="XBT", method="Bitcoin", new=False),
        list,
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
def test_get_recent_deposits_status(spot_auth_funding: Funding) -> None:
    """
    Checks the ``get_recent_deposit_status`` endpoint by executing multiple
    request with different parameters and validating its return value.
    """
    assert isinstance(spot_auth_funding.get_recent_deposits_status(), list)
    assert isinstance(spot_auth_funding.get_recent_deposits_status(asset="XLM"), list)
    assert isinstance(
        spot_auth_funding.get_recent_deposits_status(method="Stellar XLM"),
        list,
    )
    assert isinstance(
        spot_auth_funding.get_recent_deposits_status(asset="XLM", method="Stellar XLM"),
        list,
    )
    assert isinstance(
        spot_auth_funding.get_recent_deposits_status(
            asset="XLM",
            method="Stellar XLM",
            start=1688992722,
            end=1688999722,
            cursor=True,
        ),
        dict,
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_withdraw_funds(spot_auth_funding: Funding) -> None:
    """
    Checks the ``withdraw_funds`` endpoint by performing a withdraw.

    This test is disabled, because testing a withdraw cannot be done without
    a real withdraw which is not what should be done here. Also the
    API keys for testing are not allowed to withdraw or trade.
    """
    with pytest.raises(KrakenPermissionDeniedError):
        assert is_not_error(
            spot_auth_funding.withdraw_funds(
                asset="XLM",
                key="enter-withdraw-key",
                amount=10000000,
                max_fee=20,
            ),
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_get_withdrawal_info(spot_auth_funding: Funding) -> None:
    """
    Checks the ``get_withdraw_info`` endpoint by requesting the data.

    This test is disabled, because the API keys for testing are not
    allowed to withdraw or trade or even get withdraw information.
    """
    with pytest.raises(KrakenPermissionDeniedError):
        assert is_not_error(
            spot_auth_funding.get_withdrawal_info(
                asset="XLM",
                amount=10000000,
                key="enter-withdraw-key",
            ),
        )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_get_recent_withdraw_status(spot_auth_funding: Funding) -> None:
    """
    Checks the ``get_recent_withdraw_status`` endpoint using different arguments.

    This test is disabled, because testing a withdraw and receiving
    withdrawal information cannot be done without a real withdraw which is not what
    should be done here. Also the  API keys for testing are not allowed to withdraw
    or trade.
    """
    assert isinstance(spot_auth_funding.get_recent_withdraw_status(), list)
    assert isinstance(spot_auth_funding.get_recent_withdraw_status(asset="XLM"), list)
    assert isinstance(
        spot_auth_funding.get_recent_withdraw_status(method="Stellar XLM"),
        list,
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_funding()
@pytest.mark.skip(reason="CI does not have withdraw permission")
def test_wallet_transfer(spot_auth_funding: Funding) -> None:
    """
    Checks the ``get_recent_withdraw_status`` endpoint using different arguments.
    (only works if futures wallet exists)

    This test is disabled, because testing a withdraw and receiving
    withdrawal information cannot be done without a real withdraw which is not what
    should be done here. Also the  API keys for testing are not allowed to withdraw
    or trade.

    This endpoint is broken, even the provided example on the kraken doc does not work.
    """
    with pytest.raises(KrakenInvalidArgumentsError):
        assert is_not_error(
            spot_auth_funding.wallet_transfer(
                asset="XLM",
                from_="Futures Wallet",
                to_="Spot Wallet",
                amount=10000,
            ),
        )
