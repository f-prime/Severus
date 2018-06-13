from severus.db import blocks, wallet

def get_help(command):
    print ("""Severus Help

help
getaddresses

""")

def get_addresses(command):
    addresses = []
    for address in wallet.all():
        addresses.append(address['public_key'])
    print ('\n'.join(addresses))

def get_balances(command):
    pass

def main():
    commands = {
        "help":get_help,
        "getaddresses":get_addresses,
        "getbalances":get_balances
    }

    while True:
        command = input("> ")
        if command in commands:
            commands[command](command)

if __name__ == "__main__":
    main()
