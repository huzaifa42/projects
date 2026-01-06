import hashlib
import json
from time import time
class Blockchain(object):
    def __init__(self):
        self.chain=[]
        self.current_transactions=[]
        self.new_block(previous_hash=1, proof=100)
    def new_block(self, previous_hash, proof):
        """
        Docstring for new_block
        
        :param self: The proof give by proof of work algo
        :param previous_hash: hash of previous block
        :param proof: new block
        """
        block={
            'index':len(self.chain)+1,
            'timestamp':time(),
            'transaction':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])

        }
        self.current_transactions=[]
        self.chain.append(block)
        return block

    def new_trasaction(self, sender, recpient,amount):
        self.current_transactions.append({
            'sender':sender,
            'recipient':recpient,
            'amount': amount
        })
        return self.last_block['index']+1;
        
    @staticmethod
    def hash(block):
        block_string=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
