import logging

from sqlalchemy import create_engine

import config
from BlockchainUtils import BlockchainUtils
from automatization_steps import Steps
from dao import Dao
from networks import NETWORK
from rpc_client.DaemonRpcClient import DaemonRpcClient
from rpc_client.WalletRpcClient import WalletRpcClient

network = NETWORK

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
    deducibility = steps.find_output_deducibility(False)
    if deducibility is not None:
        steps.mark_deducible_rings()


try:
    while True:
        do_steps()
        steps.refresh_heights()
except KeyboardInterrupt:
    pass
