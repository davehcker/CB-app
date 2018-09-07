from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['zulu']
test_events = db['test_events']
real_events = db['real_events']
account_balances = db['balances']
