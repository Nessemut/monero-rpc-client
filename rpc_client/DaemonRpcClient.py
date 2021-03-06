from .RpcClient import RpcClient
import json
from model import Output


class DaemonRpcClient(RpcClient):

    def __init__(self, network):
        super().__init__(network.daemon_url)

    def post_json_rpc(self, method, params):
        try:
            return super().post('/json_rpc', method, params)
        except ConnectionError:
            exit('Daemon RPC not running')

    def post_other(self, context, params):
        try:
            return super().post(context, None, params)
        except ConnectionError:
            exit('Daemon RPC not running')

    def get_block_header(self, block):
        if len(str(block)) == 64:
            param = 'hash'
        else:
            param = 'height'

        params = {
            param: block
        }
        return self.post_json_rpc('get_block_header_by_' + param, params)

    def get_block(self, block):
        if len(str(block)) == 64:
            param = 'hash'
        else:
            param = 'height'

        params = {
            param: block
        }
        res = self.post_json_rpc('get_block', params)
        return json.loads(res['json'])

    def get_info(self):
        return self.post_json_rpc('get_info', None)

    def get_fee_estimate(self):
        return self.post_json_rpc('get_fee_estimate', None)

    def get_transactions(self, transactions):
        res = self.post_other('/get_transactions', {'txs_hashes': transactions, 'decode_as_json': True})['txs']
        transactions = []
        for tx in res:
            tx_dict = {}
            if not tx['in_pool']:
                try:
                    json_decoded_tx = json.loads(tx['as_json'].replace('\n', ''))
                    tx_dict.update({'tx_hash': tx['tx_hash']})
                    tx_dict.update({'block_height': tx['block_height']})
                    tx_dict.update({'block_timestamp': tx['block_timestamp']})
                    tx_dict.update({'double_spend_seen': tx['double_spend_seen']})
                    tx_dict.update({'in_pool': False})
                    tx_dict.update({'output_indices': tx['output_indices']})
                    tx_dict.update({'vin': json_decoded_tx['vin']})
                    tx_dict.update({'vout': json_decoded_tx['vout']})
                    tx_dict.update({'signatures': json_decoded_tx['signatures']})
                except KeyError:
                    pass
            else:
                # TODO: return transaction when it is not yet mined
                pass
            transactions.append(tx_dict)
        return transactions

    def get_outs(self, amount, index):
        if index is None:
            index = 0
        try:
            if amount == 0:
                res = self.post_other('/get_outs', {'outputs': [{'index': index}]})
            else:
                res = self.post_other('/get_outs', {'outputs': [{'amount': amount, 'index': index}]})
        except KeyError:
            return None
        try:
            out = res['outs'][0]
        except KeyError:
            out = None
        return out

    def is_key_image_spent(self, key_image):
        res = self.post_other('/is_key_image_spent', {'key_images': [key_image]})
        return res['spent_status'][0] == 1
