import socket
from web3 import Web3
import time

def Client_Transaction(RPC_server,pw):
    # 创建socket对象
    client_send = socket.socket()
    # 确定IP
    host = socket.gethostname()  # 获取本地主机名
    port = 12346  # 设置端口号

    client_send.connect((host, port))

    # 接受消息
    data = client_send.recv(1024)
    str1 = data.decode('UTF-8')
    Transaction = eval(str1)

    # 进行签名
    w3 = Web3(Web3.HTTPProvider(RPC_server))
    signed = w3.eth.account.sign_transaction(Transaction, pw)

    # # test
    # print(signed)
    # print(type(signed.rawTransaction))
    # print(type(signed.hash))
    # print(type(signed.r))
    # print(type(signed.s))
    # print(type(signed.v))

    # text = 'SignedTransaction(rawTransaction = HexBytes(\'' + signed.rawTransaction + '\'),hash=HexBytes(\'' + signed.hash + '\'), r=' + signed.r + ', s=' + signed.s + ', v=' + signed.v + ')'
    # print(type(text))

    # 进行分发

    b_rawTransaction = bytes(signed.rawTransaction)
    b_hash = (bytes(signed.hash))
    b_r = bytes(str(signed.r), encoding="utf8")
    b_s = bytes(str(signed.s), encoding="utf8")
    b_v = bytes(str(signed.v), encoding="utf8")

    thislist = [b_rawTransaction, b_hash, b_r, b_s, b_v]
    i = 0

    while True:

        # 发送消息

        if i == 5:
            break

        client_send.send(thislist[i])
        i = i + 1
        time.sleep(0.1)

    # 断开链接
    client_send.close()



if __name__ == '__main__':

    First_pw = 'ecf7868c95b4767e732091d0aad5203995399ce4739d20e075e8ec09765f3212'
    RPC_server = 'HTTP://127.0.0.1:7545'

    Client_Transaction(RPC_server,First_pw)

