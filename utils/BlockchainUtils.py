import logging


class BlockchainUtils:

    def __init__(self, wallet, daemon):
        self.wallet = wallet
        self.daemon = daemon

    def get_height(self):
        return self.daemon.get_info()['height']

    def get_tx_count(self):
        return self.daemon.get_info()['tx_count']

    def get_blockchain_array(self):
        height = self.get_height()
        blocks = []

        try:
            for i in range(height-1, 0, -1):
                block = self.daemon.get_block(i)
                blocks.append(block)
        except KeyboardInterrupt:
            pass

        return blocks

    @staticmethod
    def get_outputs_from_index_array(array):
        for i in range(0, len(array)):
            if i != 0:
                array[i] = array[i] + array[i-1]
        return array
