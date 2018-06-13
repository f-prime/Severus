from severus.db import blocks, wallet
from severus.user import User

def get_help(command):
    print ("""Severus Help

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

    while True:
        command = input("> ")
        if command in commands:
            commands[command](command)

if __name__ == "__main__":
    main()
