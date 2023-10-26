import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = hash

def calculate_hash(block):
    block_string = json.dumps({
        "index": block.index,
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "transactions": json.dumps(block.transactions),
        "proof": block.proof
    }, sort_keys=True)
    return hashlib.sha256(block_string.encode()).hexdigest()

def proof_of_work(last_proof):
    proof = 0
    while not is_valid_proof(last_proof, proof):
        proof += 1
    return proof

def is_valid_proof(last_proof, proof):
    guess = f"{last_proof}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"  # adjust for more/less difficulty

def create_genesis_block():
    transactions = [{"sender": "genesis", "recipient": "genesis", "amount": 0}]
    proof = proof_of_work(0)
    return Block(0, '0', time.ctime(), transactions, proof, calculate_hash(Block(0, '0', time.ctime(), transactions, proof, '')))

def create_new_block(prev_block, transactions):
    index = prev_block.index + 1
    timestamp = time.ctime()
    proof = proof_of_work(prev_block.proof)
    new_block = Block(index, prev_block.hash, timestamp, transactions, proof, '')
    new_block.hash = calculate_hash(new_block)
    return new_block

def validate_chain(blockchain):
    for i in range(1, len(blockchain)):
        current = blockchain[i]
        previous = blockchain[i - 1]

        if current.hash != calculate_hash(current):
            print(f"Block {i} has been tampered!")
            return False
        if current.previous_hash != previous.hash:
            print(f"Block {i} doesn't properly reference the previous block!")
            return False
        if not is_valid_proof(previous.proof, current.proof):
            print(f"Block {i}'s proof is invalid!")
            return False
    return True

def save_chain(blockchain, filename="blockchain.json"):
    chain_data = []
    for block in blockchain:
        chain_data.append(block.__dict__)

    with open(filename, 'w') as file:
        file.write(json.dumps(chain_data, indent=4))

def load_chain(filename="blockchain.json"):
    with open(filename, 'r') as file:
        chain_data = json.load(file)
        loaded_chain = []
        for block_data in chain_data:
            loaded_block = Block(block_data['index'], block_data['previous_hash'], block_data['timestamp'], block_data['transactions'], block_data['proof'], block_data['hash'])
            loaded_chain.append(loaded_block)
    return loaded_chain


"""
# Initialisation
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Adding blocks
for i in range(1, 10):
    transactions = [{"sender": f"user_{j}", "recipient": f"user_{j+1}", "amount": j*10} for j in range(3)]
    new_block = create_new_block(previous_block, transactions)
    blockchain.append(new_block)
    previous_block = new_block

# Save
save_chain(blockchain)

# Load
loaded_chain = load_chain()

# Validate
validation_result = validate_chain(loaded_chain)

print(validation_result)
"""
