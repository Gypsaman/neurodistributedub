from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv


def deploy():

    load_dotenv()

    with open("./SimpleStorage.sol", 'r') as file:  # change to path and name of newContract
        simple_storage_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.19"
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # change references of SimpleStorage to newContract

    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    # make sure you have your .env file set up with these variables
    w3 = Web3(Web3.HTTPProvider(os.getenv("PROVIDER")))
    print(os.getenv("PROVIDER"))
    chain_id = int(os.getenv("CHAINID"))  # Convert to int
    my_address = os.getenv("ACCOUNT")
    private_key = os.getenv("PRIVATE_KEY")

    # create a variable newContract that gets assigned a contract reference from w3.eth.contract
    newContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # create a variable nonce that gets assigned the transaction count of my_address from w3.eth.getTransactionCount
    nonce = w3.eth.get_transaction_count(my_address)

    # create a variable transaction that gets assigned the newContract.constructor().buildTransaction() method
    transaction = newContract.constructor().build_transaction({
        'from': my_address,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': nonce
    })

    # create a variable signed_txn that gets assigned the w3.eth.account.sign_transaction() method
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

    print("Deploying Contract!")
    # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt.contractAddress

if __name__ == '__main__':
    contractAddress = deploy()
    print(contractAddress)