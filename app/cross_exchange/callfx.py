from web3 import Web3
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def __host_port__(host, port):
    host_port = 'http://' + host + ':' + port
    return host_port


def callcontract(host, port, contractaddr):
    port = str(port)
    # call contract
    hp = __host_port__(host, port)
    print(hp)
    w3 = Web3(Web3.HTTPProvider(hp))
    print(w3)
    # 更换地址
    with open(os.path.join(basedir, 'walleX.abi')) as f:
        abi = json.load(f)
    print(f)
    ctr = w3.eth.contract(contractaddr, abi=abi)
    state = ctr.caller.state()
    print(state)
    print(ctr)
    return ctr, w3


def calladdlock(sourceaddr, hashstring, hexkeys, host, port, contractaddr):
    port = str(port)
    # call contract
    hp = __host_port__(host, port)
    print(hp)
    w3 = Web3(Web3.HTTPProvider(hp))
    print(w3)
    # 更换地址
    with open(os.path.join(basedir, 'walleX.abi')) as f:
        abi = json.load(f)
    print(f)
    ctr = w3.eth.contract(contractaddr, abi=abi)
    # state = ctr.caller.state()
    # print(state)
    print(ctr)
    print("s1")
    nonce = w3.eth.get_transaction_count(sourceaddr)
    print("s1")
    byteskeys = w3.toBytes(hexstr=hexkeys)
    print("s1")
    buildtr = ctr.functions.addlock(hashstring).buildTransaction({'nonce': nonce, 'from': sourceaddr, })
    print("s1")
    print(buildtr)
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    print(signed_txn)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)


def callunlock(sourceaddr, plainstring, byteskeys, host, port, contractaddr):
    port = str(port)
    # call contract
    hp = __host_port__(host, port)
    print(hp)
    w3 = Web3(Web3.HTTPProvider(hp))
    print(w3)
    # 更换地址
    with open(os.path.join(basedir, 'walleX.abi')) as f:
        abi = json.load(f)
    print(f)
    ctr = w3.eth.contract(contractaddr, abi=abi)
    # state = ctr.caller.state()
    # print(state)
    print(ctr)
    nonce = w3.eth.get_transaction_count(sourceaddr)
    buildtr = ctr.functions.unlock(plainstring).buildTransaction({'nonce': nonce, 'from': sourceaddr, })
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    calldrawmoney(sourceaddr, byteskeys, host, port, contractaddr)


def calldrawmoney(sourceaddr, byteskeys, host, port, contractaddr):
    port = str(port)
    ctr, w3 = callcontract(host, port, contractaddr)
    nonce = w3.eth.get_transaction_count(sourceaddr)
    buildtr = ctr.functions.drawmoney().buildTransaction({'nonce': nonce, 'from': sourceaddr, })
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)
