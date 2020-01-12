from .RpcClient import RpcClient
import json


class DaemonRpcClient(RpcClient):

    def __init__(self, network):
        super().__init__(network.daemon_url)

    def post(self, method, params):
        try:
            return super().post(method, params)
        except ConnectionError:
            exit('Daemon RPC not running')

    def get_block(self, block):
        if len(str(block)) == 64:
            param = 'hash'
        else:
            param = 'height'

        params = {
            param: block
        }
        res = self.post('get_block', params)
        return json.loads(res['json'])

    def get_info(self):
        return self.post('get_info', None)

    def get_fee_estimate(self):
        return self.post('get_fee_estimate', None)
