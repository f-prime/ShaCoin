import landerdb

relay = 0
brokers = [{"ip":"", "port":2525}]
version = "0.1.0"
host = ""
port = 2525
nodes = landerdb.Connect("nodes.db")
wallet = landerdb.Connect("wallet.db")
db = landerdb.Connect("db.db")
