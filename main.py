from service.DaemonRpcClient import DaemonRpcClient
from service.WalletRpcClient import WalletRpcClient
from utils.BlockchainUtils import BlockchainUtils
from networks import TESTNET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


network = TESTNET

daemon = DaemonRpcClient(network)
wallet = WalletRpcClient(network)


bc = BlockchainUtils(wallet, daemon)


engine = create_engine('sqlite:///' + network.database, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# do stuff here

session.commit()
session.close()
