import hashlib
import requests
import time

import sys


# TODO: Implement functionality to search for a proof 


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0

    def proof_of_work(last_proof):
        """
        Simple Proof of Work Algorithm
        - Find a number p' such that hash(pp') contains 6 leading
        zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """

        proof = 0
        while valid_proof(last_proof, proof) is False:
            proof += 1

        return proof
    
    def valid_proof(last_proof, proof):
        """
        Validates the Proof:  Does hash(last_proof, proof) contain 6
        leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"

    # Run forever until interrupted
    while True:
        start_time = time.time()
        # Get the last proof from the server and look for a new one
        response = requests.get('http://localhost:5000/proof')
        data = response.json()
        last_proof = data['proof']

        # When found, POST it to the server {"proof": new_proof}
        new_proof = proof_of_work(last_proof)

        print("new_proof", new_proof)

        payload = {'proof': new_proof, 'recipient': 'Brooks'}
        r = requests.post('http://localhost:5000/mine', json=payload)
        print(r.status_code)
        print(r.text)

        # TODO: If the server responds with 'New Block Forged'
        if r.status_code is 201:
            print("TO THE MOON!")
            coins_mined += 1
            print("coins:", coins_mined)
            end_time = time.time()
            print (f"Coin mined in: {end_time - start_time} seconds")
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
