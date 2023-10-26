# blockchain-app

## Emulate and play with a blockchain

This project provides an interactive simulation environment to present the core functionalities of a blockchain. 

Users can create transactions, mine new blocks, and experience how consensus algorithms work in case of conflicts between different chain states.

<img width="500" alt="a718fa8f-564b-4a92-ad29-8f069eec13de" src="https://github.com/lccopy/blockchain-app/assets/111251905/e2c1dff6-901f-4475-856d-9133b9ba3d4d">

 

## Blockchain App Interface

#### 1- Installation

Run the following command to install the required packages:

- pip install -r requirements.txt

#### 2- Usage

Start the blockchain simulation by running the following command:

- python app.py
  
On startup, a genesis block is created automatically. You can then choose to create new transactions and mine them or emulate a peer blockchain for testing the consensus algorithm (simulate peer's blockchain -> resolve to valid blockchain).

#### 3- Code Explanation

The code is divided this way:

1. Flask Web Application (app.py): This file contains the Flask web application routes and handles user interactions with the blockchain. It defines the endpoints for viewing the blockchain, creating transactions, mining new blocks, and other functionalities.

2. Blockchain Logic (utils.py): This file encapsulates the logic for creating blocks, validating the blockchain, and other core blockchain operations. It's where the essential blockchain algorithms are implemented.

3. Blockchain Data (blockchain.json): This file stores the current state of the blockchain, allowing for persistence across sessions. It gets updated whenever the blockchain is saved.


##### Core Functions

A class Block is defined to represent a block in the blockchain, which has attributes like index, previous hash, timestamp, transactions, proof of work, and hash of the block.

calculate_hash(block): Calculates the hash of a block using SHA-256 hashing algorithm.

proof_of_work(last_proof): Implements a simple proof of work algorithm by incrementing a number until the hash of the new number and the previous proof contains four leading zeros.

is_valid_proof(last_proof, proof): Validates the proof of work.

create_genesis_block(): Creates the first block of the blockchain with predefined values.

create_new_block(prev_block, transactions): Creates a new block using the information from the previous block and the new transactions.

validate_chain(blockchain): Validates the integrity of the blockchain by checking the hashes and references between consecutive blocks.

save_chain(blockchain): Saves the current state of the blockchain to a file.

load_chain(): Loads a saved blockchain from a file.






