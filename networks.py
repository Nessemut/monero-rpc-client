from NetType import NetType
import os
import config


def load_address_book(wallet_dir):
    address_book = {}

    for file in os.listdir(wallet_dir):
        if file.endswith('.bin.address.txt'):
            f = open(wallet_dir + file, "r")
            address_book.update({file.replace('.bin.address.txt', ''): f.read()})

    return address_book


MAINNET = NetType(config.MAINNET_NODE, config.MAINNET_WALLET_RPC_URL, {})

STAGENET = NetType(config.STAGENET_NODE, config.STAGENET_WALLET_RPC_URL, {})

TESTNET = NetType(config.TESTNET_NODE, config.TESTNET_WALLET_RPC_URL, load_address_book(config.TESTNET_WALLET_DIR))
