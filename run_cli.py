import sys
import severus

wallet = severus.Wallet()
try:
    wallet.load()
except:
    wallet = wallet.create()
    wallet.save()

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
    return sum([severus.calculate_funds(severus.crypto.load_pub_key(address)) for address in wallet.all_addresses()])

def create_address(command):
    w = wallet.create()
    w.save()
    return severus.crypto.save_key(w.public_key)

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
