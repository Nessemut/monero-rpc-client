from rpc_client.DaemonRpcClient import DaemonRpcClient
from rpc_client.WalletRpcClient import WalletRpcClient
from BlockchainUtils import BlockchainUtils
from networks import STAGENET
from sqlalchemy import create_engine
from dao import Dao
import config
from gc import collect
from automatization_steps import Steps

network = STAGENET

daemon = DaemonRpcClient(network)
wallet = WalletRpcClient(network)
engine = create_engine('mysql+pymysql://{}@{}/{}'.format(config.MYSQL_USER, config.MYSQL_URL, network.mysql_schema))
dao = Dao(engine)
bcutil = BlockchainUtils(wallet, daemon, network, dao)
steps = Steps(bcutil, wallet)

while True:
    steps.inject(1000)