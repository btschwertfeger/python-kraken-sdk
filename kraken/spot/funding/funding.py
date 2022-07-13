from kraken.base_api.base_api import KrakenBaseRestAPI


class FundingClient(KrakenBaseRestAPI):

    def get_deposit_methods(self, asset: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/getDepositMethods'''
        params = { 'asset': asset }
        return self._request('POST', '/private/DepositMethods', params=params)

    def get_deposit_address(self, asset: str, method: str, new: bool=False) -> dict:
        '''https://docs.kraken.com/rest/#operation/getDepositAddresses'''
        params = {
            'asset': asset,
            'method': str(method),
            'new': new
        }
        return self._request('POST', '/private/DepositAddresses', params=params)

    def get_recend_deposits_status(self, asset: str, method: str=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStatusRecentDeposits'''
        params = { 'asset': asset }
        if method != None: params['method'] = method
        return self._request('POST', '/private/DepositStatus', params=params)

    def get_withdrawal_info(self, asset: str, key: str, amount: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/getWithdrawalInformation'''
        params = {
            'asset': asset,
            'key': str(key),
            'amount': str(amount)
        }
        return self._request('POST', '/private/WithdrawInfo', params=params)

    def withdraw_funds(self, asset: str, key: str, amount: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/withdrawFund'''
        params = {
            'asset': asset,
            'key': str(key),
            'amount': str(amount)
        }
        return self._request('POST', '/private/Withdraw', params=params)

    def get_recend_withdraw_status(self, asset: str, method: str=None) -> dict:
        '''https://docs.kraken.com/rest/#operation/getStatusRecentWithdrawals'''
        params = { 'asset': asset }
        if method != None: params['method'] = method
        return self._request('POST', '/private/WithdrawStatus', params=params)

    def cancel_withdraw(self, asset: str, refid: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/cancelWithdrawal'''
        params = {
            'asset': asset,
            'refid': str(refid)
        }
        return self._request('POST', '/private/WithdrawCancel', params=params)

    def wallet_transfer(self, asset: str, from_: str, to: str, amount: str) -> dict:
        '''https://docs.kraken.com/rest/#operation/walletTransfer'''
        params = {
            'asset': asset,
            'from': from_,
            'to': to,
            'amount': amount
        }
        return self._request('POST', '/private/WalletTransfer', params=params)
