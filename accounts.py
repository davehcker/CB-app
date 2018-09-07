from web3 import Web3

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
zulu_address = '0xEFd6881AFB70E607bD0a1B33A2420E8DAd0668Ac'

abi = [ {
		"constant": True,
		"inputs": [
			{
				"name": "tokenOwner",
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
	}]

zulu_contract = web3.eth.contract(zulu_address, abi=abi)

def getBalance(contract, address):
    return contract.functions.balanceOf(address).call()


def getZuluBalance(address):
    return getBalance(zulu_contract, address)
