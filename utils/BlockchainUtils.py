from classes.Output import Output
from time import sleep
import random


class BlockchainUtils:

    def __init__(self, wallet, daemon):
        self.wallet = wallet
        self.daemon = daemon

    def get_height(self):
        return self.daemon.get_info()['height']

    def get_tx_count(self):
        return self.daemon.get_info()['tx_count']

    def get_blockchain_array(self, first, last):
        height = self.get_height()

        if first is None or first > height or first < 0:
            first = 0

        if last is None or last > height or last < first:
            last = height

        blocks = []

        try:
            for i in range(last-1, first, -1):
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

    def execute_once_a_block(self, function):
        last_updated_height = self.get_height()
        while True:
            if last_updated_height != self.get_height():
                function()
                last_updated_height = self.get_height()
            sleep(5)

    @staticmethod
    def get_all_coinbase_outputs_array(blockchain):
        output_array = []
        for block in blockchain:
            outs = block['miner_tx']['vout']
            for out in outs:
                output = Output(
                    out['target']['key'],
                    None,
                    None,
                    out['amount'],
                    None,
                    None,
                    None,
                    None
                )
                output_array.append(output)
        return output_array

    def get_incoming_transfers_output_array(self):
        output_array = []
        incoming_transfers = self.wallet.get_incoming_transfers()
        for transfer in incoming_transfers:
            output = Output(
                self.daemon.get_outs(transfer['amount'], transfer['global_index'])['key'],
                transfer['tx_hash'],
                transfer['key_image'],
                transfer['amount'],
                transfer['global_index'],
                None,
                transfer['spent'],
                None
            )
            output_array.append(output)
        return output_array
