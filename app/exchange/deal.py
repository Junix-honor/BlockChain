import web3
from web3 import Web3, IPCProvider
from decimal import *
import hashlib


# 输入信息正确情况
def is_connection(address_vps_one, address_vps_two, pw1, number, RPC_server):
    try:
        web3.HTTPProvider(RPC_server)
    except ConnectionError:
        print("Connection error")


def create_deal(address_vps_one, address_vps_two, pw1, number, RPC_server):
    w3 = Web3(Web3.HTTPProvider(RPC_server))
    print("create deal")
    amount = number  # Ether
    sending_address = address_vps_one
    receiving_address = address_vps_two

    # 打印账户的余额
    # print("Host has %f Ether" % w3.fromWei(w3.eth.getBalance(sending_address), 'ether'))
    # print("Host has %f Ether" % w3.fromWei(w3.eth.getBalance(receiving_address), 'ether'))
    # w3.personal.unlockAccount(address_vps_one, pw1)

    # 判断转账余额是否足够
    try:
        if w3.fromWei(w3.eth.getBalance(sending_address), 'ether') + Decimal.from_float(0.1) > amount:
            # 创建交易

            signed_txn = w3.eth.account.sign_transaction(dict(
                nonce=w3.eth.getTransactionCount(sending_address),
                gasPrice=w3.eth.gasPrice,
                gas=400000,  # 默认值4712388
                to=receiving_address,
                value=w3.toWei(amount, "ether"),
                data=b'',
            ),
                pw1,
            )
            try:
                tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            except:
                print("交易错误")
                return -1
            # 交易完后打印账户的余额
            # print("Host has %f Ether" % w3.fromWei(w3.eth.getBalance(sending_address), 'ether'))
            # print("Host has %f Ether" % w3.fromWei(w3.eth.getBalance(receiving_address), 'ether'))

            return w3.eth.getTransaction(tx_hash)

        else:
            print("余额不够，无法转账！请重试！")
            return -3
    except:
        print("地址错误")
        return -2


if __name__ == "__main__":
    # print(w3.isConnected())
    # print(w3.eth.accounts)
    # print("Host has %d Ether"% w3.fromWei(w3.eth.getBalance("0x8c569830D4b7A1D7bbF0E034Be2a2C095ee6f3Dd"), 'ether'))

    First_address = '0xf5e7d4Ac497af19cAF97d459048f8Efe5ac833BC'
    Second_address = '0x7E4BBD69250C1F6B21023c6a21A0F5ef836b4578'
    First_pw = 'ecf7868c95b4767e732091d0aad5203995399ce4739d20e075e8ec09765f3212'
    Second_pw = '740fffe4f5fdd194be7df8f823fbf2bc720af80def78e967ae32ea15a8d60a24'
    RPC_server = 'HTTP://127.0.0.1:7545'
    number = 12

    # 查询具体信息s
    # print(create_deal(Second_address,First_address,Second_pw,number,RPC_server))
    # 余额不足返回-3，地址错误返回-2，交易错误返回-1
    result = create_deal(First_address, Second_address, First_pw, number, RPC_server)
    print(result)
