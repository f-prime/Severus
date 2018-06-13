from severus.db import blocks, wallet
from severus.user import User
import sys

def get_help(command):
    print ("""Severus Commands

help
getaddresses
createaddress
getbalances
""")

def get_addresses(command):
    addresses = []
    for address in wallet.all():
        addresses.append(address['public_key'])
    print ('\n'.join(addresses))

def get_balances(command):
    pass

def create_address(command):
    user = User.User()
    new_user = user.create()
    new_user.save()
    print(new_user.public_key.decode())

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
        commands[command[0]](command)

if __name__ == "__main__":
    main()
