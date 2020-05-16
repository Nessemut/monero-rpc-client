import csv
import logging
from time import sleep
from collections import OrderedDict
import matplotlib.pyplot as plt

from model import Output, Ring


class BlockchainUtils:

    def __init__(self, wallet, daemon, network, dao):
        self.wallet = wallet
        self.daemon = daemon
        self.network = network
        self.dao = dao

    def get_height(self):
        return int(self.daemon.get_info()['height'])

    def get_tx_count(self):
        return self.daemon.get_info()['tx_count']

    def get_blockchain_array(self, first, last):
        height = self.get_height()

        if first is None or first > height or first < 0:
            first = 0

        if last is None or last > height or last < first:
            last = height

        blocks = []
        logging.debug('Getting blockchain from height {} to {}'.format(first, last))
        try:
            for i in range(last-1, first, -1):
                block = self.daemon.get_block(i)
                blocks.append(block)
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

    def send_one_piconero_to_myself(self):
        transfer = self.wallet.transfer(1, 11, self.wallet.address)
        return transfer is not None

    def save_output_array(self, arr):
        self.dao.save_outputs(arr)

    def plot_real_output_index_distribution(self):
        logging.info('Plotting real output distribution')
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}

        outputs = self.dao.get_known_outputs()

        rings = []

        for output in outputs:
            ring = self.dao.get_ring(output.key_image)
            if ring is not None:

                heights = []
                for ring_output in ring.outputs:
                    height = self.daemon.get_outs(None, ring_output.idx)['height']
                    heights.append(height)
                    if ring_output.key_image == ring.key_image:
                        real_height = height
                ring_tuple = (heights, real_height)
            rings.append(ring_tuple)

        logging.info(str(len(rings)) + ' own rings found')

        for ring in rings:
            ring[0].sort()
            index = ring[0].index(ring[1]) + 1
            distribution[index] += 1

        logging.info('Output age distribution in known rings is ' + str(distribution))

        plt.bar(range(len(distribution)), list(distribution.values()), align='center')
        plt.xticks(range(11), list(distribution.keys()))

        plt.ylabel('Cantidad de anillos')
        plt.xlabel('Orden de antigüedad del output real')

        plt.show()

    def write_output_age_distribution_dataset(self):
        outputs = self.dao.get_own_spent_outputs()
        own_outputs = self.dao.get_known_outputs()

        keys = []
        for output in own_outputs:
            keys.append(output.key)

        header = [
            'tx_h',
            'out1_h', 'out1_rv',
            'out2_h', 'out2_rv',
            'out3_h', 'out3_rv',
            'out4_h', 'out4_rv',
            'out5_h', 'out5_rv',
            'out6_h', 'out6_rv',
            'out7_h', 'out7_rv',
            'out8_h', 'out8_rv',
            'out9_h', 'out9_rv',
            'out10_h', 'out10_rv',
            'out11_h', 'out11_rv',
            'real'
        ]
        dataset = []

        for output in outputs:
            ring = self.dao.get_ring(output.key_image)
            if ring is not None:
                line = [ring.height]
                heights = []
                out_heights = OrderedDict()
                for ring_output in ring.outputs:
                    height = self.daemon.get_outs(None, ring_output.idx)['height']
                    heights.append(height)
                    if height not in out_heights:
                        out_heights.update({height: [ring_output.key]})
                    else:
                        out_heights[height].append(ring_output.key)
                    if ring_output.key_image == ring.key_image:
                        real_height = height
                        real_out_key = ring_output.key
                heights.sort()
                for height in sorted(out_heights.keys()):
                    for height_output in out_heights[height]:
                        line.append(height)
                        line.append(0 if height_output in keys and height_output != real_out_key else 1)

                index = heights.index(real_height) + 1
                line.append(index)
                dataset.append(line)

        filename = self.network.dataset_dir + 'ds_{}r_h{}_train.csv'.format(len(dataset), self.get_height())
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(dataset)
