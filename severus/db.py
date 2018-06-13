import tinydb

blocks = tinydb.TinyDB("blocks.db").table("blocks")
wallet = tinydb.TinyDB("wallet.db").table("wallet")
