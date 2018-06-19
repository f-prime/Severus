from severus.blockchain import Wallet
from severus.blockchain.utils.calculate_funds import calculate_funds
from severus.blockchain import crypto
import sys

wallet = Wallet()
wallet.load()

def get_help(command):
    return """Severus Commands

help
getaddresses
createaddress
getbalances
"""

def get_addresses(command):
    addresses = wallet.all_addresses()
    return '\n'.join(addresses)

def get_balances(command):
    return [calculate_funds(crypto.load_pub_key(address)) for address in wallet.all_addresses()]

def create_address(command):
    w = wallet.create()
    w.save()
    return crypto.save_key(w.public_key)

def main():
    commands = {
        "help":get_help,
        "getaddresses":get_addresses,
        "createaddress":create_address,
        "getbalances":get_balances
    }

    if len(sys.argv) < 2:
        get_help(["help"])
        sys.exit()

    command = sys.argv[1:]    

    if command[0] in commands:
        print(commands[command[0]](command))

if __name__ == "__main__":
    main()
