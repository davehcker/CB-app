from web3 import Web3
from decoder import decodeEvent
from accounts import getZuluBalance
from data import *
import time
import asyncio

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

genesis_blk_number = 3953000

#Checksummed token address
token_address = '0xEFd6881AFB70E607bD0a1B33A2420E8DAd0668Ac'

event_filter = web3.eth.filter({
    "address": token_address,
    "fromBlock": str(hex(genesis_blk_number))
})

def toPythonDict(attrDict):
    return {x: attrDict[x] for x in attrDict.keys()}

def insertEvent(event, collection):
    collection.insert_one(event)

def getAddresses(event):
    if event.get('event') == 'Transfer':
        return [event['args']['from'], event['args']['to']]

    elif event.get('event') == 'Redeem':
        return [event['args']['from']]
    else:
        return []

def updateBalance(event, collection=None):
    addresses = getAddresses(event)
    for each in addresses:
        balance = getZuluBalance(each)
        if collection:
            collection.find_one_and_update({'_id': each}, {'$set': {'balance': balance}}, upsert=True)
        else:
            print(each, balance)

def put_timestamp(event, systemTime=False):
    if systemTime==False:
        event['timestamp'] = web3.eth.getBlock(each['blockNumber'])['timestamp']
    else:
        event['timestamp'] = int(time.time())
    return event

data_logs = event_filter.get_all_entries()
data_collection = real_events
data_collection.remove({})
account_balances.remove({})

for each in data_logs:
    event = toPythonDict(decodeEvent(each))
    insertEvent(put_timestamp(event, systemTime=False), data_collection)
    updateBalance(event, account_balances)

def handle_event(event):
    insertEvent(put_timestamp(toPythonDict(decodeEvent(event)), systemTime=True), data_collection)
    updateBalance(toPythonDict(decodeEvent(event)), account_balances)

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def main():
    block_filter = web3.eth.filter({"address":token_address, 
                                    "fromBlock":str(hex(genesis_blk_number))})
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(block_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
