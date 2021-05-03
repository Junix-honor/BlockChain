import web3
from web3 import Web3, IPCProvider
from decimal import *

def Query_Balance(RPC_server,address):
    try:
        web3.HTTPProvider(RPC_server)
    except ConnectionError:
        print("Connection error")
        return 0

    w3 = Web3(Web3.HTTPProvider(RPC_server))
    balance = w3.fromWei(w3.eth.getBalance(address), 'ether')
    return balance


if __name__ == "__main__":
    RPC_server = "HTTP://127.0.0.1:7545"
    address = "0x5971E440b0b43536640d417F1502AA4F48489055"
    result = Query_Balance(RPC_server, address)
    print(round(result, 3), 'Eth')
