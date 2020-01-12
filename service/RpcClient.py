import requests
import json


class RpcClient:

    def __init__(self, url):
        self.URL = url + '/json_rpc'

    def post(self, method, params):
        data = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": method,
            "params": params
        }
        try:
            r = requests.post(self.URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            try:
                res = json.loads(r.content)['result']
                return res
            except KeyError:
                return None
        except requests.exceptions.ConnectionError:
            raise ConnectionError
