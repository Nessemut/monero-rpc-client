from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Output(Base):
    __tablename__ = 'output'
    key = Column(String, primary_key=True)
    tx = Column(String)
    key_image = Column(String)
    amount = Column(Integer)
    index = Column(Integer)
    coinbase = Column(Boolean)
    spent = Column(Boolean)
    wallet = Column(String)

    def __init__(self, key, tx, key_image, amount, index, coinbase, spent, wallet):
        self.key = key
        self.tx = tx
        self.key_image = key_image
        self.amount = amount
        self.index = index
        self.coinbase = coinbase
        self.spent = spent
        self.wallet = wallet

    def is_attr_known(self, attr):
        return self.__getattribute__(attr) is not None
