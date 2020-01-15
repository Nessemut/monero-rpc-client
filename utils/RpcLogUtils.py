from classes.Ring import Ring
import os


class RpcLogUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_user_outputs_from_log(log):
        log = open(log, 'r+')
        first = True
        all_outputs = []
        for line in log:
            if 'amount=' in line:
                if first:
                    outputs = line[line.index('indexes') + 9:len(line) - 2].split(' ')
                    real_output = line.split(',')[1][13:]
                    all_outputs.append(Ring(real_output, outputs))
                first = not first

        return all_outputs

    @classmethod
    def get_outputs_from_all_logs(cls, network):
        real_outputs_by_user = {}
        for filename in os.listdir(network.wallet_rpc_log_dir):
            user = filename.split('.')[0]
            log_file = network.wallet_rpc_log_dir + filename
            rings = cls.get_user_outputs_from_log(log_file)
            user_outputs_dict = {user: []}
            for ring in rings:
                user_outputs_dict[user].append(ring.get_real_output())
            user_outputs_dict[user].sort()
            real_outputs_by_user.update(user_outputs_dict)

        return real_outputs_by_user

    @staticmethod
    def does_output_repeat(output_arrays):
        already_checked = []
        for user in output_arrays:
            already_checked.append(user)
            for other_user in output_arrays:
                if other_user not in already_checked:
                    for output in output_arrays[user]:
                        if output in output_arrays[other_user]:
                            print('Output ' + str(output) + ' from ' + user + ' repeated in ' + other_user)
