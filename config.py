import landerdb

relay = 0
brokers = [{"ip":"zcoin.zapto.org", "port":2525}, {"ip":"192.111.130.31", "port":2525}]
version = "0.1.0"
host = ""
port = 2525
nodes = landerdb.Connect("nodes.db")
wallet = landerdb.Connect("wallet.db")
db = landerdb.Connect("db.db")
