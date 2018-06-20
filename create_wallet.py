import os

if os.path.exists("wallet.db"):
    os.remove("wallet.db")

import severus

wallet = severus.Wallet()
wallet.create().save()
