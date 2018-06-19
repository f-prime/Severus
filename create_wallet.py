import os

if os.path.exists("wallet.db"):
    os.remove("wallet.db")

from severus.blockchain import Wallet

wallet = Wallet()
wallet.create().save()
