from gc import collect

INTERVAL = 500


class Steps:

    def __init__(self, bcutil, dao, wallet):
        self.bcutil = bcutil
        self.dao = dao
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

    def mark_my_rings(self):
        my_spent_outputs = self.dao.get_own_spent_outputs()
        for output in my_spent_outputs:
            try:
                ring = self.dao.get_ring(output.key_image)
                for ring_output in ring.outputs:
                    self.dao.mark_output_in_ring(
                        ring_output,
                        ring.key_image,
                        ring_output.key_image == output.key_image,
                        True
                    )
            except AttributeError:
                # NOTE: this exception might be thrown if the ring is not yet persisted
                pass

    def mark_my_outputs_in_other_rings(self):
        my_outputs = self.dao.get_known_outputs()
        for output in my_outputs:
            self.dao.mark_output_in_ring(
                output,
                output.key_image,
                False,
                True
            )
