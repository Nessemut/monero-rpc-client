from model import Output, Ring
from time import sleep
import random
from dao import Dao


class BlockchainUtils:

    def __init__(self, wallet, daemon, network, dao):
        self.wallet = wallet
        self.daemon = daemon
        self.network = network
        self.dao = dao

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
        print('Getting blockchain from height {} to {}'.format(first, last))
        try:
            for i in range(last-1, first, -1):
                block = self.daemon.get_block(i)
                blocks.append(block)
            print('Finished')
        except KeyboardInterrupt:
            pass

        return blocks

    @staticmethod
    def get_indexes_from_offsets_array(array):
        for i in range(0, len(array)):
            if i != 0:
                array[i] = array[i] + array[i-1]
        return array

    def execute_once_a_block(self, function):
        last_updated_height = self.get_height()
        while True:
            height = self.get_height()
            if last_updated_height != height:
                print('Current block height: ' + str(height))
                function()
                last_updated_height = height
            sleep(5)

    def persist_coinbase_transactions(self, blockchain):
        output_array = []
        for block in blockchain:
            outs = block['miner_tx']['vout']
            for out in outs:
                key = out['target']['key']
                output = self.dao.get_output(key)
                if output is None:
                    output = Output(
                        out['target']['key'],
                        None,
                        out['amount'],
                        None,
                        True,
                        False,
                        None
                    )
                else:
                    output.amount = out['amount']
                    output.coinbase = True
                    output.ringct = False
                output_array.append(output)
        self.dao.save_outputs(output_array)

    def persist_incoming_transfers(self):
        output_array = []
        incoming_transfers = self.wallet.get_incoming_transfers()
        for transfer in incoming_transfers:
            # TODO: add logic to make this able to handle both v1 and v2 transactions
            key = self.daemon.get_outs(None, transfer['global_index'])['key']
            output = self.dao.get_output(key)
            if output is None:
                output = Output(
                    key,
                    transfer['key_image'],
                    transfer['amount'],
                    transfer['global_index'],
                    None,
                    None,
                    transfer['spent']
                )
            else:
                output.key_image = transfer['key_image']
                output.amount = transfer['amount'],
                output.index = transfer['global_index'],
                output.spent = transfer['spent']
            output_array.append(output)
        self.dao.save_outputs(output_array)

    def persist_rings(self, blockchain):
        for block in blockchain:
            for tx_hash in block['tx_hashes']:
                transaction = self.daemon.get_transactions([tx_hash])[0]
                inputs = transaction['vin']
                height = transaction['block_height']
                for vin in inputs:
                    out_indices = self.get_indexes_from_offsets_array(vin['key']['key_offsets'])
                    outputs = self.get_output_array_from_indices_array(out_indices)
                    key_image = vin['key']['k_image']
                    ring = Ring(key_image, tx_hash, height)
                    ring.outputs = outputs
                    self.dao.save_ring(ring)

    def get_output_array_from_indices_array(self, indices):
        outs = []
        for index in indices:
            out_json = self.daemon.get_outs(0, str(index))
            pubkey = out_json['key']
            output = self.dao.get_output(pubkey)
            if output is None:
                output = Output(pubkey, None, None, index, None, None, None)
            outs.append(output)
        return outs

    def send_one_nanonero_to_myself(self):
        transfer = self.wallet.transfer(1, 11, self.wallet.address)
        return transfer is not None

    def save_output_array(self, arr):
        self.dao.save_outputs(arr)

    def get_first_relevant_block(self):
        # TODO: return first block with a known output
        pass
