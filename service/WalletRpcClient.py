from .RpcClient import RpcClient


class WalletRpcClient(RpcClient):

    def __init__(self, network):
        super().__init__(network.wallet_url)
        self.network = network

    def post_json_rpc(self, method, params):
        try:
            return super().post('/json_rpc', method, params)
        except ConnectionError:
            exit('Wallet RPC not running')

    def get_address(self):
        return self.post_json_rpc('get_address', {'account_index': 0})['address']

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
        res = self.post_json_rpc('transfer', params)
        return res

    def get_balance(self):
        return self.post_json_rpc('get_balance', {'account_index': 0})

    def get_incoming_transfers(self):
        try:
            return self.post_json_rpc('incoming_transfers', {"transfer_type": "all", "verbose": True})['transfers']
        except KeyError:
            return None
