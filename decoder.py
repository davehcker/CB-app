from web3 import Web3
from web3.utils.events import *

transfer_event_abi = {
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "name": "from",
            "type": "address"
        },
        {
            "indexed": True,
            "name": "to",
            "type": "address"
        },
        {
            "indexed": False,
            "name": "tokens",
            "type": "uint256"
        }
    ],
    "name": "Transfer",
    "type": "event"
}

mint_event_abi = {
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "name": "treasury",
            "type": "address"
        },
        {
            "indexed": False,
            "name": "tokens",
            "type": "uint256"
        }
    ],
    "name": "Mint",
    "type": "event"
}

redeem_event_abi = {
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "name": "from",
            "type": "address"
        },
        {
            "indexed": False,
            "name": "tokens",
            "type": "uint256"
        }
    ],
    "name": "Redeem",
    "type": "event"
}

approval_event_abi = {
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "name": "tokenOwner",
            "type": "address"
        },
        {
            "indexed": True,
            "name": "spender",
            "type": "address"
        },
        {
            "indexed": False,
            "name": "tokens",
            "type": "uint256"
        }
    ],
    "name": "Approval",
    "type": "event"
}

abis = [transfer_event_abi, approval_event_abi, mint_event_abi, redeem_event_abi]
abi_topics = [event_abi_to_log_topic(x) for x in abis]


def decodeEvent(log):
    if log['topics'][0] in abi_topics:
        return get_event_data(abis[abi_topics.index(log['topics'][0])], log)
    else:
        return False

