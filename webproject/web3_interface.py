import json

import requests
from web3 import Web3

PROVIDER = "https://goerli.infura.io/v3/a6285c05a4094c4ea4a16c1395c44881"
ETHERSCAN_TOKEN = "KIHSQV61IF94K6KXEKQRJJQA41ZMK4BTR2"

nft_abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def get_nft_uri(token_addr, top=10):

    w3 = Web3(Web3.HTTPProvider(PROVIDER))

    tokenContract = None
    nfts = []
    try:
        tokenContract = w3.eth.contract(
            address=w3.toChecksumAddress(token_addr), abi=nft_abi
        )
    except:
        return nfts

    for token in range(top):
        try:
            tokenURI = tokenContract.functions.tokenURI(token).call()
        except:
            break

        if tokenURI.find("?filename") != -1:
            tokenURI = tokenURI.split("?filename")[0]
        response = requests.get(tokenURI)
        content = json.loads(response.content.decode())

        nfts.append(
            {
                "name": content["name"],
                "description": content["description"],
                "image": content["image"],
                "attributes": content["attributes"],
            }
        )

    return nfts


def get_eth_balance(account):
    EtherQuery = (
        "https://api-goerli.etherscan.io/api"
        "?module=account"
        "&action=balance"
        "&address={}"
        "&tag=latest"
        "&apikey={}"
    )

    accountquery = EtherQuery.format(account, ETHERSCAN_TOKEN)

    transinfo = json.loads(requests.get(accountquery).content.decode("utf-8"))

    balance = int(transinfo["result"]) if transinfo["message"] == "OK" else -1

    return balance / 10**18


def getEthTrans(account):

    EtherQuery = "https://api-goerli.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={}"

    accountquery = EtherQuery.format(account, ETHERSCAN_TOKEN)
    transinfo = json.loads(requests.get(accountquery).content.decode("utf-8"))
    if transinfo["message"] == "NOTOK":
        return -1

    transhist = transinfo["result"]

    return transhist


def getContracts(account):

    transhist = getEthTrans(account)
    contracts = []

    for tran in transhist:
        if tran["contractAddress"] > "":
            contracts.append(tran["contractAddress"])

    return contracts


def getContractCreator(contract):

    transactions = getEthTrans(contract)

    if transactions == -1:
        return "Invalid"

    for tran in transactions:
        if tran["contractAddress"].lower() == contract.lower():
            return tran["from"]
