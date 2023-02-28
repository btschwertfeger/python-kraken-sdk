"""Module that implements the Kraken Futures Funding client"""
from kraken.base_api.base_api import KrakenBaseFuturesAPI


class FundingClient(KrakenBaseFuturesAPI):
    """Class that implements the Kraken Futures Funding client"""

    def __init__(
        self, key: str = "", secret: str = "", url: str = "", sandbox: bool = False
    ) -> None:
        super().__init__(key=key, secret=secret, url=url, sandbox=sandbox)

    def get_historical_funding_rates(self, symbol: str) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-historical-funding-rates-historicalfundingrates"""
        return self._request(
            method="GET",
            uri="/derivatives/api/v4/historicalfundingrates",
            query_params={"symbol": symbol},
            auth=False,
        )

    def initiate_wallet_transfer(
        self, amount: str, fromAccount: str, toAccount: str, unit: str
    ) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-wallet-transfer"""
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/transfer",
            post_params={
                "amount": amount,
                "fromAccount": fromAccount,
                "toAccount": toAccount,
                "unit": unit,
            },
            auth=True,
        )

    def initiate_subccount_transfer(
        self,
        amount: str,
        fromAccount: str,
        fromUser: str,
        toAccount: str,
        toUser: str,
        unit: str,
    ) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-sub-account-transfer"""
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/transfer/subaccount",
            post_params={
                "amount": amount,
                "fromAccount": fromAccount,
                "fromUser": fromUser,
                "toAccount": toAccount,
                "toUser": toUser,
                "unit": unit,
            },
            auth=True,
        )

    def initiate_withdrawal_to_spot_wallet(
        self, amount: str, currency: str, sourceWallet: str = None, **kwargs
    ) -> dict:
        """https://docs.futures.kraken.com/#http-api-trading-v3-api-transfers-initiate-withdrawal-to-spot-wallet"""
        if self.sandbox:
            raise ValueError("This function is not available in sandbox mode.")
        params = {
            "amount": str(amount),
            "currency": currency,
        }
        if sourceWallet is not None:
            params["sourceWallet"] = sourceWallet
        params.update(kwargs)
        return self._request(
            method="POST",
            uri="/derivatives/api/v3/withdrawal",
            post_params=params,
            auth=True,
        )
