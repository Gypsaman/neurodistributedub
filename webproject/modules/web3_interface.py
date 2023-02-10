import json
from datetime import datetime as dt

import requests
from web3 import Web3
import os
from webproject.modules.dotenv_util import initialize_dotenv

initialize_dotenv()

PROVIDER = os.getenv("PROVIDER")
ETHERSCAN_TOKEN = os.getenv("ETHERSCAN_TOKEN")

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
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
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
        except Exception as e:
            break

        if tokenURI.find("?filename") != -1:
            tokenURI = tokenURI.split("?filename")[0]
        else:
            tokenURI = tokenURI.split("filename")[0]
        response = requests.get(tokenURI)
        if response.status_code != 200:
            break
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


def get_contract_abi(account):
    EtherQuery = (
        "https://api-goerli.etherscan.io/api"
        "?module=contract"
        "&action=getabi"
        "&address={}"
        "&apikey={}"
    )

    accountquery = EtherQuery.format(account, ETHERSCAN_TOKEN)

    transinfo = json.loads(requests.get(accountquery).content.decode("utf-8"))
    
    print(transinfo)

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
    
    try:
        transinfo = json.loads(requests.get(accountquery).content.decode("utf-8"))
    except:
        return -1

    balance = int(transinfo["result"]) if transinfo["message"] == "OK" else -1

    return balance / 10**18


def getEthTrans(account):

    EtherQuery = "https://api-goerli.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={}"

    #without offset (limit 10)
    EtherQuery = "https://api-goerli.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&page=1&sort=asc&apikey={}"

    accountquery = EtherQuery.format(account, ETHERSCAN_TOKEN)
    transinfo = json.loads(requests.get(accountquery).content.decode("utf-8"))
    if transinfo["message"] == "NOTOK":
        return -1

    transhist = transinfo["result"]
    transhist = conform_eth_trans(transhist)
    return transhist


def conform_eth_trans(transhist):
    for tran in transhist:
        tran["trans_from"] = tran["from"]
        del tran["from"]
        tran["trans_to"] = tran["to"]
        del tran["to"]
        tran["timeStamp"] = dt.fromtimestamp(int(tran["timeStamp"]))
        tran["isError"] = tran["isError"] != "0"
        tran["txreceipt_status"] = tran["txreceipt_status"] != "0"
    return transhist


def getContracts(account):
    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    
    transhist = getEthTrans(account)
    contracts = []

    for tran in transhist:
        contract = tran["contractAddress"]
        contract_type = 'NFT'
        if contract > "":
            try:
                tokenContract = w3.eth.contract(
                    address=w3.toChecksumAddress(contract), abi=nft_abi
                )
            except:
                continue
            
            try:
                tokenContract.functions.tokenURI(0).call()
            except:
                try:
                    bal = tokenContract.functions.balanceOf(w3.toChecksumAddress(contract)).call()
                    contract_type = 'ERC20'
                except Exception as e:
                    contract_type = 'DAPP'

            contracts.append({"contract":contract,"type":contract_type})

    return contracts


def getContractCreator(contract):

    transactions = getEthTrans(contract)

    if transactions == -1:
        return "Invalid"

    for tran in transactions:
        if tran["contractAddress"].lower() == contract.lower():
            return tran["trans_from"]
    
    return "Invalid"


def CallContractFunction(contract, func, args):
    w3 = Web3(Web3.HTTPProvider(PROVIDER))
    contract = w3.eth.contract(address=contract, abi=nft_abi)
    func = getattr(contract.functions, func)
    return func(*args).call()
