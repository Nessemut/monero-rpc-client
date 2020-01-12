from .RpcClient import RpcClient
import config


class WalletRpcClient(RpcClient):

    def __init__(self, network):
        super().__init__(network.wallet_url)
        self.network = network

    def post(self, method, params):
        try:
            return super().post(method, params)
        except ConnectionError:
            exit('Wallet RPC not running')

    def transfer(self, amount, ring_size, dest):
        try:
            wallet = self.network.address_book[dest]
        except KeyError:
            exit('User ' + dest + ' does not exist')
        params = {
            "destinations": [
                {"amount": amount,
                 "address": wallet
                 }
            ],
            "account_index": 0,
            "subaddr_indices": [0],
            "priority": 0,
            "ring_size": ring_size,
            "get_tx_key": True
        }
        res = self.post('transfer', params)
        print('Sent ' + str(res['amount']) + ' piconero in transaction ' + res['tx_hash'])

    def get_balance(self):
        return self.post('get_balance', {'account_index': 0})
