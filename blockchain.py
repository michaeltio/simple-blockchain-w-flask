import datetime
import hashlib
import json
from flask import Flask, jsonify


#Building Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {
            "index" : len(self.chain) + 1,
            "timestamp" : str(datetime.datetime.now()),
            "proof" : proof,
            "previous_hash" : previous_hash
        }

        self.chain.append(block)
        return block
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                print("Proof found:", new_proof)
                print("Hash:", hash_operation)
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # ini buat ngecheck buat memastikan kalau block n-1 di hash itu sama dengan atribute hash previous block yang ada di block n
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # sekarang buat ngecheck kalo yang nge hash itu beneran sesuai dengan kriteria diffuculty sekarang
            previous_block = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_block**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True

#Mining Blockchain
# Create Web App
app = Flask(__name__)
#Create Blockchain
blockchain = Blockchain()

# Mining New Block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message' : 'Congratulations, your just mined a block!', 
        'index' : block['index'],
        'timestamp' : block['timestamp'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/check_chain',  methods = ['GET'])
def check_chain():
    isValid = blockchain.is_chain_valid(blockchain.chain)
    response = {
        'valid' : isValid
    } 
    return jsonify(response), 200
# Running app

app.run(host='0.0.0.0',port = 5000)