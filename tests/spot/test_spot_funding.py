# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# All rights reserved.
# https://github.com/btschwertfeger
#

"""Module that implements the unit tests for the Spot funding client."""

from typing import Any, Self

import pytest

from kraken.exceptions import KrakenInvalidArgumentsError, KrakenPermissionDeniedError
from kraken.spot import Funding

from .helper import is_not_error


@pytest.mark.spot
@pytest.mark.spot_auth
@pytest.mark.spot_funding
class TestSpotFunding:
    """Test class for Spot Funding client functionality."""

    TEST_ASSET_BTC = "XBT"
    TEST_ASSET_XLM = "XLM"
    TEST_ASSET_USD = "ZUSD"
    TEST_METHOD_BITCOIN = "Bitcoin"
    TEST_METHOD_STELLAR = "Stellar XLM"
    TEST_METHOD_BANK_FRICK = "Bank Frick (SWIFT)"
    TEST_WITHDRAW_KEY = "enter-withdraw-key"
    TEST_AMOUNT_LARGE = 10000000
    TEST_AMOUNT_MEDIUM = 10000
    TEST_MAX_FEE = 20
    TEST_START_TIME = 1688992722
    TEST_END_TIME = 1688999722

    def _assert_successful_list_response(
        self: Self,
        result: Any,  # noqa: ANN401
    ) -> None:
        """Helper method to assert successful list responses."""
        assert isinstance(result, list)

    def _assert_successful_dict_response(
        self: Self,
        result: Any,  # noqa: ANN401
    ) -> None:
        """Helper method to assert successful dict responses."""
        assert isinstance(result, dict)

    def _assert_not_error(self: Self, result: Any) -> None:  # noqa: ANN401
        """Helper method to assert responses without errors."""
        assert is_not_error(result)

    def test_get_deposit_methods(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks if the response of the ``get_deposit_methods`` is of
        type list which mean that the request was successful.
        """
        result = spot_auth_funding.get_deposit_methods(asset=self.TEST_ASSET_BTC)
        self._assert_successful_list_response(result)

    def test_get_deposit_address(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the ``get_deposit_address`` function by performing a valid request
        and validating that the response is of type list.
        """
        result = spot_auth_funding.get_deposit_address(
            asset=self.TEST_ASSET_BTC,
            method=self.TEST_METHOD_BITCOIN,
            new=False,
        )
        self._assert_successful_list_response(result)

    def test_get_recent_deposits_status(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the ``get_recent_deposit_status`` endpoint by executing multiple
        request with different parameters and validating its return value.
        """
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_deposits_status(),
        )
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_deposits_status(asset=self.TEST_ASSET_XLM),
        )
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_deposits_status(
                method=self.TEST_METHOD_STELLAR,
            ),
        )
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_deposits_status(
                asset=self.TEST_ASSET_XLM,
                method=self.TEST_METHOD_STELLAR,
            ),
        )
        self._assert_successful_dict_response(
            spot_auth_funding.get_recent_deposits_status(
                asset=self.TEST_ASSET_XLM,
                method=self.TEST_METHOD_STELLAR,
                start=self.TEST_START_TIME,
                end=self.TEST_END_TIME,
                cursor=True,
            ),
        )

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_withdraw_funds(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the ``withdraw_funds`` endpoint by performing a withdraw.

        This test is disabled, because testing a withdraw cannot be done without
        a real withdraw which is not what should be done here. Also the
        API keys for testing are not allowed to withdraw or trade.
        """
        with pytest.raises(KrakenPermissionDeniedError):
            result = spot_auth_funding.withdraw_funds(
                asset=self.TEST_ASSET_XLM,
                key=self.TEST_WITHDRAW_KEY,
                amount=self.TEST_AMOUNT_LARGE,
                max_fee=self.TEST_MAX_FEE,
            )
        self._assert_not_error(result)

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_get_withdrawal_info(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the ``get_withdraw_info`` endpoint by requesting the data.

        This test is disabled, because the API keys for testing are not
        allowed to withdraw or trade or even get withdraw information.
        """
        with pytest.raises(KrakenPermissionDeniedError):
            result = spot_auth_funding.get_withdrawal_info(
                asset=self.TEST_ASSET_XLM,
                amount=self.TEST_AMOUNT_LARGE,
                key=self.TEST_WITHDRAW_KEY,
            )
        self._assert_not_error(result)

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_get_recent_withdraw_status(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the ``get_recent_withdraw_status`` endpoint using different arguments.

        This test is disabled, because testing a withdraw and receiving
        withdrawal information cannot be done without a real withdraw which is not what
        should be done here. Also the  API keys for testing are not allowed to withdraw
        or trade.
        """
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_withdraw_status(),
        )
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_withdraw_status(asset=self.TEST_ASSET_XLM),
        )
        self._assert_successful_list_response(
            spot_auth_funding.get_recent_withdraw_status(
                method=self.TEST_METHOD_STELLAR,
            ),
        )

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_wallet_transfer(self: Self, spot_auth_funding: Funding) -> None:
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
            result = spot_auth_funding.wallet_transfer(
                asset=self.TEST_ASSET_XLM,
                from_="Futures Wallet",
                to_="Spot Wallet",
                amount=self.TEST_AMOUNT_MEDIUM,
            )
        self._assert_not_error(result)

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_withdraw_methods(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the withdraw_methods function for retrieving the correct data type
        which is sufficient to validate the functionality.
        """
        response = spot_auth_funding.withdraw_methods()
        self._assert_successful_list_response(response)

        response = spot_auth_funding.withdraw_methods(
            asset=self.TEST_ASSET_USD,
            aclass="currency",
        )
        self._assert_successful_list_response(response)

        response = spot_auth_funding.withdraw_methods(
            asset=self.TEST_ASSET_BTC,
            network=self.TEST_METHOD_BITCOIN,
        )
        self._assert_successful_list_response(response)

        response = spot_auth_funding.withdraw_methods(aclass="forex")
        self._assert_successful_list_response(response)

    @pytest.mark.skip(reason="Tests do not have withdraw permission")
    def test_withdraw_addresses(self: Self, spot_auth_funding: Funding) -> None:
        """
        Checks the withdraw_addresses function for retrieving the correct data type
        which is sufficient to validate the functionality.
        """
        response = spot_auth_funding.withdraw_addresses()
        self._assert_successful_list_response(response)

        response = spot_auth_funding.withdraw_addresses(
            asset=self.TEST_ASSET_USD,
            method=self.TEST_METHOD_BANK_FRICK,
        )
        self._assert_successful_list_response(response)

        response = spot_auth_funding.withdraw_addresses(
            asset=self.TEST_ASSET_XLM,
            verified=True,
        )
        self._assert_successful_list_response(response)
