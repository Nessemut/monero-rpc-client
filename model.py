from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


association_table = Table(
    'association', Base.metadata,
    Column('output_pubkey', String, ForeignKey('output.key')),
    Column('ring_ki', String, ForeignKey('ring.key_image')),
    Column('real', Boolean)
)


class Output(Base):
    __tablename__ = 'output'
    key = Column(String, primary_key=True)
    key_image = Column(String)
    amount = Column(Integer)
    index = Column(Integer)
    coinbase = Column(Boolean)
    ringct = Column(Boolean)
    spent = Column(Boolean)
    sender = Column(String)
    recipient = Column(String)
    rings = relationship(
        "Ring",
        secondary=association_table,
        back_populates="outputs")

    def __init__(self, key, key_image, amount, index, coinbase, ringct, spent, sender, recipient):
        self.key = key
        self.key_image = key_image
        self.amount = amount
        self.index = index
        self.coinbase = coinbase
        self.ringct = ringct
        self.spent = spent
        self.sender = sender
        self.recipient = recipient

    def is_attr_known(self, attr):
        return self.__getattribute__(attr) is not None


class Ring(Base):
    __tablename__ = 'ring'
    key_image = Column(String, primary_key=True)
    outputs = relationship(
        "Output",
        secondary=association_table,
        back_populates="rings")

    def __init__(self, key, tx, key_image):
        self.key = key
        self.tx = tx
        self.key_image = key_image
