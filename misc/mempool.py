from web3 import Web3

# Connect to the Ethereum network
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a6285c05a4094c4ea4a16c1395c44881'))

pending = w3.geth.txpool.inspect()

print(pending)