import hashlib
from collections import UserList
from datetime import datetime


'''
Adapted from:
https://github.com/howCodeORG/Simple-Python-Blockchain/blob/master/blockchain.py
'''


class Block:

    _number = 0
    _data = None
    _timestamp = None
    # nonce is adjusted by miners so that the hash of the block will be less
    # than or equal to the current target of the network.
    _nonce = 0
    _previous_hash = 0x0

    @property
    def nonce(self):
        return self._nonce

    @nonce.setter
    def nonce(self, var):
        self._nonce = var

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, var):
        self._number = var

    @property
    def data(self):
        return self._data

    def __init__(self, data):
        self._data = data
        self._timestamp = datetime.now()

    def generate_hash(self):
        h = hashlib.sha256()
        h.update(
            str(self._nonce).encode('utf-8') +
            str(self._data).encode('utf-8') +
            str(self._previous_hash).encode('utf-8') +
            str(self._timestamp).encode('utf-8') +
            str(self._number).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.generate_hash()) + \
            "\nNumber: " + str(self._number) + \
            "\nBlock Data: " + str(self.data) + \
            "\nBlock Creation Time: " + str(self._timestamp) + \
            "\nHashes: " + str(self._nonce) + "\n" + 80*"-"


class Blockchain(UserList):

    # increasing this value takes longer
    difficulty = 10
    max_nonce = 2**32
    target = 2 ** (256-difficulty)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        block = Block("Genesis")
        super().append(block)

    def append(self, block):
        block.previous_hash = self.data[-1].generate_hash()
        block.number = self.__len__()
        super().append(block)

    def mine(self, block):
        '''
        This simulates de the bitcoin mining
        '''
        print("* Mining block containing the data:\n\n{}".format(block.data))
        for _ in range(self.max_nonce):
            if int(block.generate_hash(), 16) <= self.target:
                print("** Appending the block to the BlockChain")
                self.append(block)
                break
            else:
                block.nonce += 1


def main():

    blockchain = Blockchain()

    # Create, mine and add the blocks to the block chain
    for i in range(1, 11):
        blockchain.mine(Block("Block Data " + str(i)))

    # prints the blocks
    print('\n\n' + 80*'*' + '\n\n')
    for i in blockchain:
        print(i)


if __name__ == "__main__":
    main()
