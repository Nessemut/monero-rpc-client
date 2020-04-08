from gc import collect
import logging
import random

INTERVAL = 500


class Steps:

    def __init__(self, bcutil, dao, wallet):
        self.bcutil = bcutil
        self.dao = dao
        self.wallet = wallet
        self.working_height = self.bcutil.get_height()
        self.last_persisted_height = self.dao.last_persisted_ring()
        logging.getLogger('Steps')

    def refresh_heights(self):
        self.working_height = self.bcutil.get_height()
        self.last_persisted_height = self.dao.last_persisted_ring()

    def inject(self):
        logging.info('Injecting outputs')
        n = random.randrange(100, 10000)
        count = 0
        for i in range(0, n):
            if self.bcutil.send_one_nanonero_to_myself():
                count += 1
            if i % 25 == 0:
                self.wallet.rescan_blockchain()
        logging.info(str(count) + ' one nanonero outputs injected')

    def persist_outputs(self):
        logging.info('Persisting outputs from height {} to {}'.format(self.last_persisted_height, self.working_height))
        for i in range(self.last_persisted_height, self.working_height, INTERVAL):
            blocks = self.bcutil.get_blockchain_array(i, i+INTERVAL-1)
            self.bcutil.persist_coinbase_transactions(blocks)
            collect()

        self.bcutil.persist_incoming_transfers()

    def persist_rings(self):
        logging.info('Persisting rings from height {} to {}'.format(self.last_persisted_height, self.working_height))
        for i in range(self.last_persisted_height, self.working_height, INTERVAL):
            blocks = self.bcutil.get_blockchain_array(i, i+INTERVAL-1)
            self.bcutil.persist_rings(blocks)

    def mark_my_rings(self):
        logging.info('Marking realness of outputs in own rings')
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
        logging.info('Marking own decoy outputs as false')
        my_outputs = self.dao.get_known_outputs()
        for output in my_outputs:
            self.dao.mark_output_in_ring(
                output,
                output.key_image,
                False,
                False
            )

    def mark_rings_by_process_of_elimination(self):
        # logging.info('Searching for rings to mark by process of elimination')
        # logging.info('{} new rings deduced')
        pass

    def mark_outputs_from_deduced_rings(self):
        pass

    def generate_report(self):
        pass
