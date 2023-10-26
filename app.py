from flask import Flask, jsonify, request, render_template, redirect, url_for
from utils import *
import random

app = Flask(__name__)

# global blockchain variable
blockchain = [create_genesis_block()]
pending_transactions = []  # store transactions b4 mining

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", blockchain=blockchain)

@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'POST':
        values = request.form

        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        transaction = {
            'sender': values['sender'],
            'recipient': values['recipient'],
            'amount': float(values['amount']),
        }
        pending_transactions.append(transaction)

        return redirect(url_for('index'))

    return render_template("new_transaction.html")

@app.route('/mine', methods=['GET', 'POST'])
def mine():
    if request.method == 'POST':
        last_block = blockchain[-1]
        new_block = create_new_block(last_block, pending_transactions[:])

        # reset list  once mined
        del pending_transactions[:]

        blockchain.append(new_block)
        return render_template("mine.html", new_block=new_block)

    return render_template("mine.html", new_block=None)

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = []
    for block in blockchain:
        chain_data.append(block.__dict__)

    return jsonify({'chain': chain_data, 'length': len(blockchain)}), 200

@app.route('/validate', methods=['GET'])
def validate():
    if validate_chain(blockchain):
        return jsonify({'message': 'The blockchain is valid!'}), 200
    else:
        return jsonify({'message': 'The blockchain is compromised!'}), 400

@app.route('/save', methods=['GET'])
def save():
    save_chain(blockchain)
    return jsonify({'message': 'Blockchain saved successfully!'}), 200

@app.route('/load', methods=['GET'])
def load():
    global blockchain
    blockchain = load_chain()
    return jsonify({'message': 'Blockchain loaded successfully!'}), 200

@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if index < 0 or index >= len(blockchain):
        return jsonify({'message': 'Block not found!'}), 404
    block = blockchain[index]
    return jsonify(block.__dict__), 200



peer_blockchain = [] # list of emulated peer interactions

@app.route('/simulate_peer', methods=['GET'])
def simulate_peer():
    global peer_blockchain
    peer_blockchain = [create_genesis_block()]
    previous_block = peer_blockchain[0]

    # add blocks to the peer blockchain
    for i in range(1, random.randint(2, 100)):  #peer has a longer chain
        transactions = [{"sender": f"peer_{j}", "recipient": f"peer_{j+1}", "amount": random.randint(1, 50000)} for j in range(3)]
        new_block = create_new_block(previous_block, transactions)
        peer_blockchain.append(new_block)
        previous_block = new_block

    return jsonify({'message': 'Peer blockchain simulated!'}), 200

@app.route('/resolve', methods=['GET'])
def resolve():
    global blockchain
    if len(peer_blockchain) > len(blockchain):
        blockchain = peer_blockchain
        return jsonify({'message': 'Blockchain replaced with the peer\'s longer chain!'}), 200
    else:
        return jsonify({'message': 'Our blockchain is the valid one!'}), 200






if __name__ == "__main__":
    app.run(debug=False)
