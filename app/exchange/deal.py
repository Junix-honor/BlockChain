import binascii

import web3
from web3 import Web3, IPCProvider
from decimal import *
import socket



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
                print('####################')
                print(signed_txn.rawTransaction)
                print('####################')
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
    # result = create_deal(First_address, Second_address, First_pw, number, RPC_server)
    # print(result)



    # w3 = Web3(Web3.HTTPProvider(RPC_server))
    #
    # s = socket.socket()
    # host = socket.gethostname()
    # port = 12345
    # s.bind((host,port))
    #
    # s.listen(5)
    # while True:
    #     c,addr = s.accept()
    #     print ('连接地址:',addr)
    #
    #     Transaction = dict(
    #             nonce=w3.eth.getTransactionCount(First_address),
    #             gasPrice=w3.eth.gasPrice,
    #             gas=400000,  # 默认值4712388
    #             to=Second_address,
    #             value=w3.toWei(number, "ether"),
    #             data=b'',
    #         )
    #     #字典需先转换为json，后转换为byte
    #     str = str(Transaction)
    #     b_deal = str.encode('UTF-8')
    #     c.send(b_deal)
    #     data = []
    #     i=0
    #
    #
    #     text = bytes.decode(c.recv(1024))
    #     print(text)
    #     print(type(text))

    #     s_rawTransaction = hexbytes.HexBytes(b_rawTransaction.hex())
    #     s_hash = hexbytes.HexBytes(b_hash.hex())
    #     print(b_rawTransaction)
    #     print(s_hash)
    #
    #     s_r = int().from_bytes(b_r, byteorder='big', signed=True)
    #     s_s = int().from_bytes(b_s, byteorder='big', signed=True)
    #     s_v = int().from_bytes(b_v, byteorder='big', signed=True)
    #     print(s_r)
    #     print(s_s)
    #     print(s_v)
    #
    #     text = 'SignedTransaction(rawTransaction = HexBytes(\'' + s_rawTransaction + '\'),hash=HexBytes(\'' + s_hash + '\'), r=' + str(s_r) + ', s=' + str(s_s) + ', v=' + str(s_v) + ')'
    #     print(type(text))
    #
    #
     #tx_hash = w3.eth.sendRawTransaction(text.rawTransaction)
