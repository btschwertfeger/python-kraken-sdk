'''Module that implements the Kraken Spot Stakung client'''
from kraken.base_api.base_api import KrakenBaseSpotAPI
class StakingClient(KrakenBaseSpotAPI):
    '''Class that implements the Kraken Spot Stakung client'''

    def stake_asset(self, asset: str, amount: str, method: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/stake'''
        return self._request(
            method='POST',
            uri='/private/Stake',
            params={
                'asset': asset,
                'amount': amount,
                'method': method
            },
            auth=True
        )

    def unstake_asset(self, asset: str, amount: str, method: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/unstake'''
        return self._request(
            method='POST',
            uri='/private/Unstake',
            params={
                'asset': asset,
                'amount': amount,
                'method': method
            }, auth=True
        )

    def list_stakeable_assets(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingAssetInfo'''
        return self._request(
            method='POST',
            uri='/private/Staking/Assets',
            auth=True
        )

    def get_pending_staking_transactions(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingPendingDeposits'''
        return self._request(
            method='POST',
            uri='/private/Staking/Pending',
            auth=True
        )

    def list_staking_transactions(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingTransactions'''
        return self._request(
            method='POST',
            uri='/private/Staking/Transactions',
            auth=True
        )
