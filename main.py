from rpc_client.DaemonRpcClient import DaemonRpcClient
from rpc_client.WalletRpcClient import WalletRpcClient
from BlockchainUtils import BlockchainUtils
from networks import STAGENET
from sqlalchemy import create_engine
from dao import Dao
import config
from gc import collect

network = STAGENET

daemon = DaemonRpcClient(network)
wallet = WalletRpcClient(network)
engine = create_engine('mysql+pymysql://{}@{}/{}'.format(config.MYSQL_USER, config.MYSQL_URL, network.mysql_schema))
dao = Dao(engine)
bcutil = BlockchainUtils(wallet, daemon, network, dao)


def inject(n):
    for i in range(0, n):
        bcutil.send_one_nanonero_to_myself()


def persist_outputs():
    height = int(bcutil.get_height())
    interval = 5000
    for i in range(0, height, interval):
        blocks = bcutil.get_blockchain_array(i, i+interval-1)
        bcutil.persist_coinbase_transactions(blocks)
        collect()

    bcutil.persist_incoming_transfers()


def persist_rings():
    height = int(bcutil.get_height())
    interval = 10
    for i in range(137000, height, interval):
        blocks = bcutil.get_blockchain_array(i, i+interval-1)
        bcutil.persist_rings(blocks)


def get_blockchain():
    blocks = bcutil.get_blockchain_array(None, None)
    return blocks

