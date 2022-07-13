from kraken.base_api.base_api import KrakenBaseRestAPI

class StakingClient(KrakenBaseRestAPI):

    def stake_asset(self, asset: str, amount: str, method: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/stake'''
        params = {
            'asset': asset,
            'amount': amount,
            'method': method
        }
        return self._request('POST', '/private/Stake', params=params)

    def unstake_asset(self, asset: str, amount: str, method: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/unstake'''
        params = {
            'asset': asset,
            'amount': amount
        }
        return self._request('POST', '/private/Unstake', params=params)

    def list_stakeable_assets(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingAssetInfo'''
        return self._request('POST', '/private/Staking/Assets')

    def get_pending_staking_transactions(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingPendingDeposits'''
        return self._request('POST', '/private/Staking/Pending')

    def list_staking_transactions(self) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStakingTransactions'''
        return self._request('POST', '/private/Staking/Transactions')

