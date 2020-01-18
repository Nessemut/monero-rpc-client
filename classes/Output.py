class Output:

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
        print(self.__getattribute__(attr))
        return self.__getattribute__(attr) is not None
