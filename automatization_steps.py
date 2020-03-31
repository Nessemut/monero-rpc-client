from gc import collect

INTERVAL = 500


class Steps:

    def __init__(self, bcutil, wallet):
        self.bcutil = bcutil
        self.wallet = wallet

    def inject(self, n):
        for i in range(0, n):
            self.bcutil.send_one_nanonero_to_myself()
            if i % 25 == 0:
                self.wallet.rescan_blockchain()

    def persist_outputs(self, start_block):
        height = int(self.bcutil.get_height())
        for i in range(start_block, height, INTERVAL):
            blocks = self.bcutil.get_blockchain_array(i, i+INTERVAL-1)
            self.bcutil.persist_coinbase_transactions(blocks)
            collect()

        self.bcutil.persist_incoming_transfers()

    def persist_rings(self, start_block):
        height = int(self.bcutil.get_height())
        for i in range(start_block, height, INTERVAL):
            blocks = self.bcutil.get_blockchain_array(i, i+INTERVAL-1)
            self.bcutil.persist_rings(blocks)

