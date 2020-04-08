from rpc_client.DaemonRpcClient import DaemonRpcClient
from rpc_client.WalletRpcClient import WalletRpcClient
from BlockchainUtils import BlockchainUtils
from networks import STAGENET
from sqlalchemy import create_engine
from dao import Dao
import config
from gc import collect
from automatization_steps import Steps
import logging

network = STAGENET

daemon = DaemonRpcClient(network)
wallet = WalletRpcClient(network)
engine = create_engine('mysql+pymysql://{}@{}/{}'.format(config.MYSQL_USER, config.MYSQL_URL, network.mysql_schema))
dao = Dao(engine)
bcutil = BlockchainUtils(wallet, daemon, network, dao)
steps = Steps(bcutil, dao, wallet)

logger = logging
logger.basicConfig(level=config.LOGGING_LEVEL)
logger.getLogger(__name__)

logger.info('Monero RPC Client started')


def do_steps():
    steps.inject()
    steps.persist_outputs()
    steps.persist_rings()
    steps.mark_my_rings()
    steps.mark_my_outputs_in_other_rings()
    # TODO: steps below not yet implemented
    steps.mark_rings_by_process_of_elimination()
    steps.mark_outputs_in_deduced_rings()
    steps.generate_report()

try:
    while True:
        do_steps()
        steps.refresh_heights()
except KeyboardInterrupt:
    pass
