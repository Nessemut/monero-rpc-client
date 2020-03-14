from NetType import NetType
import config


MAINNET = NetType(
    config.MAINNET_NODE,
    config.MAINNET_WALLET_RPC_URL,
    config.MAINNET_FILES_BASE_DIR,
    config.MAINNET_MYSQL_SCHEMA
)

STAGENET = NetType(
    config.STAGENET_NODE,
    config.STAGENET_WALLET_RPC_URL,
    config.STAGENET_FILES_BASE_DIR,
    config.STAGENET_MYSQL_SCHEMA
)

TESTNET = NetType(
    config.TESTNET_NODE,
    config.TESTNET_WALLET_RPC_URL,
    config.TESTNET_FILES_BASE_DIR,
    config.TESTNET_MYSQL_SCHEMA
)
