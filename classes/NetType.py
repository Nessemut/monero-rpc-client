import os


class NetType:

    def __init__(self, daemon_url, wallet_url, base_dir):
        self.daemon_url = daemon_url
        self.wallet_url = wallet_url
        self.wallet_dir = base_dir + '/wallets/'
        self.wallet_rpc_log_dir = base_dir + '/wallet-rpc-logs/'
        self.address_book = self.load_address_book()

    def load_address_book(self):
        address_book = {}

        for file in os.listdir(self.wallet_dir):
            if file.endswith('.address.txt'):
                f = open(self.wallet_dir + file, "r")
                address_book.update({file.replace('.bin', '').replace('.address.txt', ''): f.read()})

        return address_book
