#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that tests the Kraken Spot REST endpoints"""
import os
import random
import time
import unittest
from datetime import datetime, timezone

import pytest

from kraken.exceptions.exceptions import KrakenExceptions
from kraken.spot.client import Funding, Market, Staking, Trade, User


def is_not_error(value) -> bool:
    """Returns True if 'error' in dict."""
    return isinstance(value, dict) and "error" not in value


class UserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__auth_user = User(
            key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY")
        )

    def test_get_account_balance(self) -> None:
        assert is_not_error(self.__auth_user.get_account_balance())

    def test_get_balances(self):
        assert is_not_error(self.__auth_user.get_balances(currency="USD"))

    def test_get_trade_balance(self) -> None:
        assert is_not_error(self.__auth_user.get_trade_balance())
        assert is_not_error(self.__auth_user.get_trade_balance(asset="EUR"))

    def test_get_open_orders(self) -> None:
        assert is_not_error(self.__auth_user.get_open_orders(trades=True))
        assert is_not_error(
            self.__auth_user.get_open_orders(trades=False, userref="1234567")
        )

    def test_get_closed_orders(self) -> None:
        assert is_not_error(self.__auth_user.get_closed_orders())
        assert is_not_error(
            self.__auth_user.get_closed_orders(trades=True, userref="1234")
        )
        assert is_not_error(
            self.__auth_user.get_closed_orders(trades=True, start="1668431675.4778206")
        )
        assert is_not_error(
            self.__auth_user.get_closed_orders(
                trades=True, start="1668431675.4778206", end="1668455555.4778206", ofs=2
            )
        )
        assert is_not_error(
            self.__auth_user.get_closed_orders(
                trades=True,
                start="1668431675.4778206",
                end="1668455555.4778206",
                ofs=1,
                closetime="open",
            )
        )

    def test_get_orders_info(self) -> None:
        for params, method in zip(
            [
                {"txid": "OXBBSK-EUGDR-TDNIEQ"},
                {"txid": "OXBBSK-EUGDR-TDNIEQ", "trades": True},
                {"txid": "OQQYNL-FXCFA-FBFVD7"},
                {"txid": ["OE3B4A-NSIEQ-5L6HW3", "O23GOI-WZDVD-XWGC3R"]},
            ],
            [
                self.__auth_user.get_orders_info,
                self.__auth_user.get_orders_info,
                self.__auth_user.get_trades_info,
                self.__auth_user.get_trades_info,
            ],
        ):
            try:
                assert is_not_error(method(**params))
            except KrakenExceptions.KrakenInvalidOrderError:
                pass
            finally:
                time.sleep(1.5)

    def test_get_trades_history(self) -> None:
        assert is_not_error(
            self.__auth_user.get_trades_history(type_="all", trades=True)
        )
        assert is_not_error(
            self.__auth_user.get_trades_history(
                type_="closed position",
                start="1677717104",
                end="1677817104",
                ofs="1",
            )
        )

    def test_get_open_positions(self) -> None:
        assert isinstance(self.__auth_user.get_open_positions(), list)
        assert isinstance(
            self.__auth_user.get_open_positions(txid="OQQYNL-FXCFA-FBFVD7"), list
        )
        assert isinstance(
            self.__auth_user.get_open_positions(
                txid="OQQYNL-FXCFA-FBFVD7", docalcs=True
            ),
            list,
        )

    def test_get_ledgers_info(self) -> None:
        assert is_not_error(self.__auth_user.get_ledgers_info())
        assert is_not_error(self.__auth_user.get_ledgers_info(type_="deposit"))
        assert is_not_error(
            self.__auth_user.get_ledgers_info(
                asset="EUR", start="1668431675.4778206", end="1668455555.4778206", ofs=2
            )
        )
        assert is_not_error(
            self.__auth_user.get_ledgers_info(
                asset=["EUR", "USD"],
            )
        )
        assert is_not_error(
            self.__auth_user.get_ledgers_info(
                asset="EUR,USD",
            )
        )

    def test_get_ledgers(self) -> None:
        assert is_not_error(self.__auth_user.get_ledgers(id_="LNYQGU-SUR5U-UXTOWM"))
        assert is_not_error(
            self.__auth_user.get_ledgers(
                id_=["LNYQGU-SUR5U-UXTOWM", "LTCMN2-5DZHX-6CPRC4"], trades=True
            )
        )

    def test_get_trade_volume(self) -> None:
        assert is_not_error(self.__auth_user.get_trade_volume())
        assert is_not_error(
            self.__auth_user.get_trade_volume(pair="DOT/EUR", fee_info=False)
        )

    def test_request_save_export_report(self) -> None:
        try:
            self.__auth_user.request_export_report(
                report="invalid", description="this is an invalid report type"
            )
        except ValueError:
            # invalid report type
            pass

        for report in ("trades", "ledgers"):
            if report == "trades":
                fields = [
                    "ordertxid",
                    "time",
                    "ordertype",
                    "price",
                    "cost",
                    "fee",
                    "vol",
                    "margin",
                    "misc",
                    "ledgers",
                ]
            else:
                fields = [
                    "refid",
                    "time",
                    "type",
                    "aclass",
                    "asset",
                    "amount",
                    "fee",
                    "balance",
                ]

            export_descr = f"{report}-export-{random.randint(0, 10000)}"
            response = self.__auth_user.request_export_report(
                report=report,
                description=export_descr,
                fields=fields,
                format_="CSV",
                starttm="1662100592",
                endtm=int(1000 * time.time()),
            )
            assert is_not_error(response) and "id" in response
            time.sleep(2)

            status = self.__auth_user.get_export_report_status(report=report)
            assert isinstance(status, list)
            time.sleep(5)

            result = self.__auth_user.retrieve_export(id_=response["id"])
            with open(f"{export_descr}.zip", "wb") as file:
                for chunk in result.iter_content(chunk_size=512):
                    if chunk:
                        file.write(chunk)

            status = self.__auth_user.get_export_report_status(report=report)
            assert isinstance(status, list)
            for response in status:
                assert "id" in response
                try:
                    assert isinstance(
                        self.__auth_user.delete_export_report(
                            id_=response["id"], type_="delete"
                        ),
                        dict,
                    )
                except (
                    Exception
                ):  # '200 - {"error":["WDatabase:No change"],"result":{"delete":true}}'
                    pass
                time.sleep(2)

    def test_export_report_status(self) -> None:
        # just demonstrating invalid report; real test is in `test_request_save_export_report` function
        try:
            self.__auth_user.get_export_report_status(report="invalid")
        except ValueError:
            pass

    def tearDown(self) -> None:
        return super().tearDown()


class MarketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__market = Market()

    def test_get_system_status(self) -> None:
        assert is_not_error(self.__market.get_system_status())

    def test_get_assets(self) -> None:
        for params in [
            {},
            {"assets": "USD"},
            {"assets": ["USD"]},
            {"assets": ["XBT", "USD"]},
            {"assets": ["XBT", "USD"], "aclass": "currency"},
        ]:
            assert is_not_error(self.__market.get_assets(**params))
            time.sleep(1.5)

    def test_get_tradable_asset_pair(self) -> None:
        assert is_not_error(self.__market.get_tradable_asset_pair(pair="BTCUSD"))
        assert is_not_error(
            self.__market.get_tradable_asset_pair(pair=["DOTEUR", "BTCUSD"])
        )
        for i in ("info", "leverage", "fees", "margin"):
            assert is_not_error(
                self.__market.get_tradable_asset_pair(pair="DOTEUR", info=i)
            )
            break

    def test_get_ticker(self) -> None:
        assert is_not_error(self.__market.get_ticker())
        assert is_not_error(self.__market.get_ticker(pair="XBTUSD"))
        assert is_not_error(self.__market.get_ticker(pair=["DOTUSD", "XBTUSD"]))

    def test_get_ohlc(self) -> None:
        assert is_not_error(self.__market.get_ohlc(pair="XBTUSD"))
        assert is_not_error(
            self.__market.get_ohlc(pair="XBTUSD", interval=240, since="1616663618")
        )  # interval in [1 5 15 30 60 240 1440 10080 21600]

    def test_get_order_book(self) -> None:
        assert is_not_error(self.__market.get_order_book(pair="XBTUSD"))
        assert is_not_error(
            self.__market.get_order_book(pair="XBTUSD", count=2)
        )  # count in [1...500]

    def test_get_recent_trades(self) -> None:
        assert is_not_error(self.__market.get_recent_trades(pair="XBTUSD"))
        assert is_not_error(
            self.__market.get_recent_trades(pair="XBTUSD", since="1616663618")
        )

    def test_get_recend_spreads(self) -> None:
        assert is_not_error(self.__market.get_recend_spreads(pair="XBTUSD"))
        assert is_not_error(
            self.__market.get_recend_spreads(pair="XBTUSD", since="1616663618")
        )

    def tearDown(self) -> None:
        return super().tearDown()


class TradeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__auth_trade = Trade(
            key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY")
        )

    # @unittest.skip('Skipping Spot test_create_order endpoint')
    def test_create_order(self) -> None:
        try:
            assert isinstance(
                self.__auth_trade.create_order(
                    ordertype="limit",
                    side="buy",
                    volume=1,
                    oflags=["post"],
                    pair="BTC/EUR",
                    price=0.01,
                    timeinforce="GTC",
                    validate=True,  # important to just test this endpoint without risking money
                ),
                dict,
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

        try:
            assert isinstance(
                self.__auth_trade.create_order(
                    ordertype="limit",
                    side="buy",
                    volume=10000000,
                    oflags=["post"],
                    pair="BTC/EUR",
                    price=0.01,
                    expiretm="0",
                    displayvol=1000,
                    validate=True,  # important to just test this endpoint without risking money
                ),
                dict,
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

        try:
            assert isinstance(
                self.__auth_trade.create_order(
                    ordertype="stop-loss",
                    side="buy",
                    volume="1000",
                    trigger="last",
                    pair="XBTUSD",
                    price="100",
                    price2="120",
                    leverage="2",
                    userref="12345",
                    close_ordertype="limit",
                    close_price="123",
                    close_price2="92",
                    validate=True,
                ),
                dict,
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

        try:
            self.__auth_trade.create_order(
                ordertype="stop-loss-limit",
                side="buy",
                volume="1000",
                trigger="index",
                pair="XBTUSD",
                price="100",
                price2="80",
                timeinforce="GTC",
                validate=True,
            )
        except ValueError:
            # cannot use trigger and timeinforce together
            pass

    def test_create_order_batch(self) -> None:
        assert isinstance(
            self.__auth_trade.create_order_batch(
                orders=[
                    {
                        "close": {
                            "ordertype": "stop-loss-limit",
                            "price": 120,
                            "price2": 110,
                        },
                        "ordertype": "limit",
                        "price": 140,
                        "price2": 130,
                        "timeinforce": "GTC",
                        "type": "buy",
                        "userref": "345dsdfddfgdsgdfgsfdsfsdf",
                        "volume": 1000,
                    },
                    {
                        "ordertype": "limit",
                        "price": 150,
                        "timeinforce": "GTC",
                        "type": "sell",
                        "userref": "1dfgesggwe5t3",
                        "volume": 123,
                    },
                ],
                pair="BTC/USD",
                validate=True,  # important
            ),
            dict,
        )

    def test_edit_order(self) -> None:
        print(str(datetime.now(timezone.utc).isoformat()))
        try:
            assert isinstance(
                self.__auth_trade.edit_order(
                    txid="OHYO67-6LP66-HMQ437",
                    userref="12345678",
                    volume=1.25,
                    pair="XBTUSD",
                    price=27500,
                    price2=26500,
                    cancel_response=False,
                    oflags=["post"],
                    validate=True,
                ),
                dict,
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

    def test_cancel_order(self) -> None:
        try:
            assert isinstance(
                self.__auth_trade.cancel_order(txid="O2JLFP-VYFIW-35ZAAE"), dict
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

    @unittest.skip("Skipping Spot test_cancel_all_orders endpoint")
    def test_cancel_all_orders(self) -> None:
        try:
            assert isinstance(self.__auth_trade.cancel_all_orders(), dict)
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

    @unittest.skip("Skipping Spot test_cancel_all_orders_after_x endpoint")
    def test_cancel_all_orders_after_x(self) -> None:
        try:
            assert isinstance(
                self.__auth_trade.cancel_all_orders_after_x(timeout=6), dict
            )
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

    def test_cancel_order_batch(self) -> None:
        assert isinstance(
            self.__auth_trade.cancel_order_batch(
                orders=[
                    "O2JLFP-VYFIW-35ZAAE",
                    "O523KJ-DO4M2-KAT243",
                    "OCDIAL-YC66C-DOF7HS",
                    "OVFPZ2-DA2GV-VBFVVI",
                ]
            ),
            dict,
        )

    def tearDown(self) -> None:
        return super().tearDown()


class StakingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__auth_staking = Staking(
            key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY")
        )

    def test_list_stakeable_assets(self) -> None:
        try:
            assert isinstance(self.__auth_staking.list_stakeable_assets(), list)
        except KrakenExceptions.KrakenPermissionDeniedError:
            pass

    @unittest.skip("Skipping Spot test_stake_asset endpoint")
    def test_stake_asset(self) -> None:
        try:
            assert is_not_error(
                self.__auth_staking.stake_asset(
                    asset="DOT", amount="4500000", method="polkadot-staked"
                )
            )
        except KrakenExceptions.KrakenInvalidAmountError:
            pass

    @unittest.skip("Skipping Spot test_unstake_asset endpoint")
    def test_unstake_asset(self) -> None:
        try:
            assert is_not_error(
                self.__auth_staking.unstake_asset(asset="DOT", amount="4500000")
            )
        except KrakenExceptions.KrakenInvalidAmountError:
            pass

    @unittest.skip("Skipping Spot test_get_pending_staking_transactions endpoint")
    def test_get_pending_staking_transactions(self) -> None:
        assert isinstance(self.__auth_staking.get_pending_staking_transactions(), list)

    @unittest.skip("Skipping Spot test_list_staking_transactions endpoint")
    def test_list_staking_transactions(self) -> None:
        assert isinstance(self.__auth_staking.list_staking_transactions(), list)

    def tearDown(self) -> None:
        return super().tearDown()


class FundingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.__auth_funding = Funding(
            key=os.getenv("SPOT_API_KEY"), secret=os.getenv("SPOT_SECRET_KEY")
        )

    def test_get_deposit_methods(self) -> None:
        assert isinstance(self.__auth_funding.get_deposit_methods(asset="XBT"), list)

    def test_get_deposit_address(self) -> None:
        assert isinstance(
            self.__auth_funding.get_deposit_address(
                asset="XBT", method="Bitcoin", new=False
            ),
            list,
        )

    def test_get_recend_deposits_status(self) -> None:
        assert isinstance(
            self.__auth_funding.get_recend_deposits_status(asset="XLM"), list
        )
        assert isinstance(
            self.__auth_funding.get_recend_deposits_status(
                asset="XLM", method="Stellar XLM"
            ),
            list,
        )

    # @unittest.skip("Skipping Spot test_withdraw_funds endpoint")
    def test_withdraw_funds(self) -> None:
        # CI API Keys are not allowd to withdraw, trade and cancel
        with pytest.raises(KrakenExceptions.KrakenPermissionDeniedError):
            assert is_not_error(
                self.__auth_funding.withdraw_funds(
                    asset="XLM", key="enter-withdraw-key", amount=10000000
                )
            )

    # @unittest.skip("Skipping Spot test_get_withdrawal_info endpoint")
    def test_get_withdrawal_info(self) -> None:
        # CI API Keys are not allowd to withdraw, trade and cancel
        with pytest.raises(KrakenExceptions.KrakenPermissionDeniedError):
            assert is_not_error(
                self.__auth_funding.get_withdrawal_info(
                    asset="XLM", amount=10000000, key="enter-withdraw-key"
                )
            )

    # @unittest.skip("Skipping Spot test_get_recend_withdraw_status endpoint")
    def test_get_recend_withdraw_status(self) -> None:
        assert isinstance(
            self.__auth_funding.get_recend_withdraw_status(asset="XLM"), list
        )
        # CI API Keys are not allowd to withdraw, trade and cancel
        with pytest.raises(KrakenExceptions.KrakenPermissionDeniedError):
            assert is_not_error(
                self.__auth_funding.cancel_withdraw(
                    asset="XLM", refid="AUBZC2T-6WMDG2-HYWFC7"
                )
            )  # only works with real refid

    # @unittest.skip("Skipping Spot test_wallet_transfer endpoint")
    def test_wallet_transfer(self) -> None:
        # CI API Keys are not allowd to withdraw, trade and cancel
        # this endpoint is broken, even the provided example on the kraken doc does not work
        with pytest.raises(KrakenExceptions.KrakenInvalidArgumentsError):
            # only works if futures wallet exists
            assert is_not_error(
                self.__auth_funding.wallet_transfer(
                    asset="XLM", from_="Futures Wallet", to_="Spot Wallet", amount=10000
                )
            )

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
