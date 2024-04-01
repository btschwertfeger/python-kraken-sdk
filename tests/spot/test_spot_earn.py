#!/usr/bin/env python
# Copyright (C) 2024 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot Earn client."""

import pytest

from kraken.spot import Earn

from .helper import is_not_error


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_allocate_earn_funds(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``allocate_earn_funds`` is of
    type bool which mean that the request was successful.
    """
    assert isinstance(
        spot_auth_earn.allocate_earn_funds(
            amount="1",
            strategy_id="ESRFUO3-Q62XD-WIOIL7",
        ),
        bool,
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_deallocate_earn_funds(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``deallocate_earn_funds`` is of
    type bool which mean that the request was successful.
    """
    assert isinstance(
        spot_auth_earn.deallocate_earn_funds(
            amount="1",
            strategy_id="ESRFUO3-Q62XD-WIOIL7",
        ),
        bool,
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_get_allocation_status(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``get_allocation_status`` does not contain a
    named error which mean that the request was successful.
    """
    assert is_not_error(
        spot_auth_earn.get_allocation_status(
            strategy_id="ESRFUO3-Q62XD-WIOIL7",
        ),
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_get_deallocation_status(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``get_deallocation_status`` does not contain a
    named error which mean that the request was successful.
    """
    assert is_not_error(
        spot_auth_earn.get_deallocation_status(
            strategy_id="ESRFUO3-Q62XD-WIOIL7",
        ),
    )


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_list_earn_strategies(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``list_earn_strategies`` does not contain a
    named error which mean that the request was successful.
    """
    assert is_not_error(spot_auth_earn.list_earn_strategies(asset="DOT"))


@pytest.mark.spot()
@pytest.mark.spot_auth()
@pytest.mark.spot_earn()
@pytest.mark.skip(reason="CI does not have earn permission")
def test_list_earn_allocations(spot_auth_earn: Earn) -> None:
    """
    Checks if the response of the ``list_earn_allocations`` does not contain a
    named error which mean that the request was successful.
    """
    assert is_not_error(spot_auth_earn.list_earn_allocations(asset="DOT"))
