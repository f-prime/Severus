import severus

wallet = severus.Wallet()
wallet.load()

print(severus.Transaction.create(wallet.public_key, 23).verify())
