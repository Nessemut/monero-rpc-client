from service.DaemonRpcClient import DaemonRpcClient
from service.WalletRpcClient import WalletRpcClient
from BlockchainUtils import BlockchainUtils
from networks import MAINNET, STAGENET, TESTNET


network = TESTNET

daemon = DaemonRpcClient(network)
wallet = WalletRpcClient(network)


bc = BlockchainUtils(wallet, daemon)
