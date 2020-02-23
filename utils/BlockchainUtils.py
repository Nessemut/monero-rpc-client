from classes.Output import Output
from time import sleep
import random


class BlockchainUtils:

    def __init__(self, wallet, daemon, network):
        self.wallet = wallet
        self.daemon = daemon
        self.network = network

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
        total = last-first
        try:
            for i in range(last-1, first, -1):
                if i % 100 == 0:
                    print(-i-first/total)
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
            height = self.get_height()
            if last_updated_height != height:
                print('Current block height: ' + str(height))
                function()
                last_updated_height = height
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
                    None,
                    None
                )
                output_array.append(output)
        return output_array

    def get_incoming_transfers_output_array(self):
        output_array = []
        incoming_transfers = self.wallet.get_incoming_transfers()
        for transfer in incoming_transfers:
            # TODO: add logic to make this able to handle both v1 and v2 transactions
            output = Output(
                self.daemon.get_outs(None, transfer['global_index'])['key'],
                transfer['tx_hash'],
                transfer['key_image'],
                transfer['amount'],
                transfer['global_index'],
                None,
                transfer['spent'],
                None,
                self.wallet.address
            )
            output_array.append(output)
        return output_array

    def send_random_transactions(self):
        times = random.randint(1, 10)
        for i in range(0, times):
            amount = random.randint(1, 1000000)
            recipient = random.choice(list(self.network.address_book.keys()))
            transfer = self.wallet.transfer(amount, 11, self.network.address_book[recipient])
            if transfer is not None:
                print('Sent ' + str(amount) + ' moneroj in tx ' + transfer['tx_hash'] + ' to ' + recipient)
            else:
                print('Could not send transaction')

    def send_one_nanonero_to_myself(self):
        return self.wallet.transfer(1, 11, self.wallet.address)
