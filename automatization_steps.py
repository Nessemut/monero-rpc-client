import collections
import logging
from gc import collect
import matplotlib.pyplot as plt


INTERVAL = 500


class Steps:

    def __init__(self, bcutil, dao, wallet):
        self.bcutil = bcutil
        self.dao = dao
        self.wallet = wallet
        self.working_height = self.bcutil.get_height()
        self.last_persisted_height = self.dao.last_persisted_ring()

    def refresh_heights(self):
        self.working_height = self.bcutil.get_height()
        self.last_persisted_height = self.dao.last_persisted_ring()

    def inject(self):
        logging.info('Injecting outputs')
        count = 0
        try:
            while True:
                if self.bcutil.send_one_piconero_to_myself():
                    count += 1
                if count % 25 == 0:
                    self.wallet.rescan_blockchain()
        except KeyboardInterrupt:
            logging.info(str(count) + ' one piconero outputs injected')

    def persist_outputs(self):
        logging.info('Saving outputs from height {} to {}'.format(self.last_persisted_height, self.working_height))
        for i in range(self.last_persisted_height, self.working_height, INTERVAL):
            blocks = self.bcutil.get_blockchain_array(i, i+INTERVAL-1)
            self.bcutil.persist_coinbase_transactions(blocks)
            collect()

        self.bcutil.persist_incoming_transfers()

    def persist_rings(self):
        logging.info('Saving rings from height {} to {}'.format(self.last_persisted_height, self.working_height))
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

    def find_output_deducibility(self, plot):
        # TODO: move this plotting logic somewhere else

        logging.info('Looking for foreign rings with known outputs')

        report = {}
        key_images = self.dao.other_rings_with_at_least_one_own_decoy()
        deducible_outputs = []

        for ki in key_images:
            remaining = self.dao.get_remaining_outputs_from_ring_with_decoys(ki[0])
            if remaining not in report:
                report[remaining] = 1
            else:
                report[remaining] = report[remaining] + 1
            if remaining == 0:
                deducible_outputs.append(ki)

        report = collections.OrderedDict(sorted(report.items()))
        output_line = 'Foreign rings with known decoys:'
        for key in report:
            output_line = output_line + '\n\t {} rings with {} outputs remaining to be deducible'\
                .format(report[key], key)
        logging.info(output_line)

        if plot:
            plt.bar(range(len(report)), list(report.values()), align='center')
            plt.xticks(range(10), list(report.keys()))

            plt.yscale('log')
            plt.ylabel('Cantidad de anillos')
            plt.xlabel('Outputs restantes para deducir anillo')

            plt.show()

        return deducible_outputs if len(deducible_outputs) > 0 else None

    def mark_deducible_rings(self):
        # TODO: implement this when some deducible rings are found
        pass
