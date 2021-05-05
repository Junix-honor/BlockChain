import commands
import os
import sys
from web3 import Web3
import json


def callsh(sourceaddr, destinaddr, value, host, port):
    value = value*1000000000000000000
    cmm = 'bash /root/WXtest0419/starter'+' '+sourceaddr+' '+destinaddr+' '+str(value)+' '+host+' '+port
    status, out = commands.getstatusoutput(cmm)
    print(out)
    loca = out.find('contract address:    0')
    ca = out[loca:loca+63]
    print(ca)
    addrstart = ca.find('0')
    contraddr = ca[addrstart:]
    # print(contraddr)
    return contraddr

def __host_port__(host,port):
    host_port = host + ':' + port
    return host_port

def callcontract(host,port,contractaddr):
    # call contract
    hp=__host_port__(host,port)
    w3 = Web3(Web3.HTTPProvider(hp))
    #更换地址
    with open('walleX.abi') as f:
        abi = json.load(f)
    ctr=w3.eth.contract(contractaddr, abi=abi)

def calladdlock(sourceaddr,hashstring,hexkeys):
    nonce = w3.eth.get_transaction_count(sourceaddr)
    byteskeys = w3.toBytes(hexstr=hexkeys)
    buildtr=ctr.functions.addlock(hashstring).buildTransaction({'nonce':nonce,})
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

def callunlock(sourceaddr,plainstring,byteskeys):
    nonce = w3.eth.get_transaction_count(sourceaddr)
    buildtr=ctr.functions.unlock(plainstring).buildTransaction({'nonce':nonce,'from':sourceaddr,})
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

def calldrawmoney(sourceaddr,byteskeys):
    nonce = w3.eth.get_transaction_count(sourceaddr)
    buildtr=ctr.functions.drawmoney().buildTransaction({'nonce':nonce,'from':sourceaddr,})
    signed_txn = w3.eth.account.sign_transaction(buildtr, private_key=byteskeys)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)



