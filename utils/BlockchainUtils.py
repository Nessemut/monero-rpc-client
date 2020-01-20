from classes.Output import Output


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

    def get_all_coinbase_outputs_array(self, blockchain):
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
