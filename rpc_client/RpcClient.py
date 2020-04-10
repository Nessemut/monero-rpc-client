import json

import requests


class RpcClient:

    def __init__(self, url):
        self.URL = url

    @staticmethod
    def json_rpc_result(res):
        return res['result']

    @staticmethod
    def other_result(res):
        result = {}
        for o in res:
            if o != 'status' and o != 'untrusted':
                result.update({o: res[o]})
        return result

    def post(self, context, method, params):
        if context == '/json_rpc':
            data = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": method,
                "params": params
            }
            extract_result = self.json_rpc_result
        else:
            data = params
            extract_result = self.other_result

        try:
            r = requests.post(self.URL + context, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            try:
                return extract_result(json.loads(r.content))
            except KeyError:
                return None
        except requests.exceptions.ConnectionError:
            raise ConnectionError
