from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


association_table = Table(
    'association_table', Base.metadata,
    Column('output_pubkey', String, ForeignKey('output.key')),
    Column('ring_ki', String, ForeignKey('ring.key_image')),
    Column('real', Boolean)
)


class Output(Base):
    __tablename__ = 'output'
    key = Column(String, primary_key=True, unique=True, nullable=False)
    key_image = Column(String)
    amount = Column(Integer)
    idx = Column(Integer)
    coinbase = Column(Boolean, nullable=True, default=None)
    ringct = Column(Boolean, nullable=True, default=None)
    spent = Column(Boolean, nullable=True, default=None)

    def __init__(self, key, key_image, amount, index, coinbase, ringct, spent):
        self.key = key
        self.key_image = key_image
        self.amount = amount
        self.idx = index
        self.coinbase = coinbase
        self.ringct = ringct
        self.spent = spent

    def is_attr_known(self, attr):
        return self.__getattribute__(attr) is not None


class Ring(Base):
    __tablename__ = 'ring'
    key_image = Column(String, primary_key=True, unique=True, nullable=False)
    transaction = Column(String)
    height = Column(Integer)
    outputs = relationship(
        "Output",
        secondary=association_table,
        lazy='joined')

    def __init__(self, key_image, transaction, height):
        self.key_image = key_image
        self.transaction = transaction
        self.height = height
