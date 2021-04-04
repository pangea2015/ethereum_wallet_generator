'''
depends on module: "eth-account"
installation: 
python -m pip install eth-account
'''

# import
from eth_account import Account
from os import urandom
import urllib.request
from json import load
from argparse import ArgumentParser
from time import sleep

# functions
def generate_acc():
    global acc
    acc = Account.create(urandom(256))
    return acc

def gen_output():
    generate_acc()
    if args.quiet == 1:
        if args.balance:
            print(acc.privateKey.hex(), acc.address, get_balance() + " ETH")
        else:
            print(acc.privateKey.hex(), acc.address)
    elif args.quiet == 2:
        print(acc.privateKey.hex())
    elif args.quiet == 3:
        print(acc.address)
    elif args.quiet >= 4:
        print(get_balance())
    else:
        if args.quietbalance:
            if int(get_balance()) > 0:
                print(acc.privateKey.hex(), acc.address, get_balance() + " ETH")
        else:
            print(f"\nPrivate Key: {acc.privateKey.hex()}\nAdress: {acc.address}")
            if args.balance:
                print(f"Balance: {get_balance()} ETH")

def get_balance():
    global acc
    with open("api_key.ini", "r") as key:
            if key.read() == "":
                    call = urllib.request.urlopen(f"https://api.etherscan.io/api?module=account&action=balance&address={str(acc.address)}&tag=latest")
                    balance = load(call)["result"]
                    try:
                        return balance
                    finally:
                        sleep(4.9)
            else:
                for line in key.read():
                    call = urllib.request.urlopen(f"https://api.etherscan.io/api?module=account&action=balance&address={str(acc.address)}&tag=latest&apikey={str(line)}")
                    balance = load(call)["result"]
                    try:
                        return balance
                    finally:
                        sleep(0.2)
                    


# argparse
parser = ArgumentParser(description="A tool to generate valid Ethereum Wallets", prog="Ethereum Wallet Generator")
parser.add_argument("-b", "--balance", help="If specified, checks the balance of each generated wallet. | SLOWS DOWN A LOT", action="store_true")

gen_wallet = parser.add_mutually_exclusive_group()
gen_wallet.add_argument("-gen", "--generateWallets", metavar="NUMBER", help="generates a given number of wallets with private and public key", type=int)
gen_wallet.add_argument("-geninf", "--generateInfinite", help="generates random wallets forever | -q recommended | CTRL + C to stop", action="store_true")

outprint = parser.add_mutually_exclusive_group()
outprint.add_argument("-q", "--quiet", help="prints only the output | -qq -qqq -qqqq for even less output", action="count", default=0)
outprint.add_argument("-qb", "--quietbalance", help="only prints ETH Adresses with balance > 0 | propably won't find anything | useful for output to file", action="store_true")

args = parser.parse_args()

# code
if args.generateInfinite:
    while True:
        gen_output()

if args.generateWallets != None and args.generateWallets > 0:
    if args.quiet == 0:
        for wallet in range(int(args.generateWallets)):
            gen_output()
    else:
        for wallet in range(int(args.generateWallets)):
            gen_output()

# if opened directly
if __name__ == "__main__":
    if not any(vars(args).values()):
        gen_output()
