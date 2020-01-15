from classes.NetType import NetType
import config

MAINNET = NetType(
    config.MAINNET_NODE,
    config.MAINNET_WALLET_RPC_URL,
    config.MAINNET_FILES_BASE_DIR
)

STAGENET = NetType(
    config.STAGENET_NODE,
    config.STAGENET_WALLET_RPC_URL,
    config.STAGENET_FILES_BASE_DIR
)

TESTNET = NetType(
    config.TESTNET_NODE,
    config.TESTNET_WALLET_RPC_URL,
    config.TESTNET_FILES_BASE_DIR
)
