import config
from NetType import NetType

MAINNET = NetType(
    config.MAINNET_NODE,
    config.MAINNET_WALLET_RPC_URL,
    config.FILES_BASE_DIR + '/mainnet',
    config.MAINNET_MYSQL_SCHEMA
)

STAGENET = NetType(
    config.STAGENET_NODE,
    config.STAGENET_WALLET_RPC_URL,
    config.FILES_BASE_DIR + '/stagenet',
    config.STAGENET_MYSQL_SCHEMA
)

TESTNET = NetType(
    config.TESTNET_NODE,
    config.TESTNET_WALLET_RPC_URL,
    config.FILES_BASE_DIR + '/testnet',
    config.TESTNET_MYSQL_SCHEMA
)


NETWORKS = {
    'TESTNET': TESTNET,
    'STAGENET': STAGENET,
    'MAINNET': MAINNET
}

NETWORK = NETWORKS[config.ACTIVE_NETWORK]
