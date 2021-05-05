    # 创建socket对象

from web3 import Web3
import socket
import hexbytes
from eth_account.datastructures import SignedTransaction

def Server_Transaction(RPC_server,From_address, To_address, number):
    w3 = Web3(Web3.HTTPProvider(RPC_server))

    server_receive = socket.socket()

    # bind()绑定
    host = socket.gethostname()
    port = 12346
    server_receive.bind((host, port))
    # listen监听
    server_receive.listen(5)
    # 建立客户端链接
    # accept 接受请求链接
    conn, addr = server_receive.accept()

    # send Transaction
    Transaction = dict(
        nonce=w3.eth.getTransactionCount(From_address),
        gasPrice=w3.eth.gasPrice,
        gas=400000,  # 默认值4712388
        to=To_address,
        value=w3.toWei(number, "ether"),
        data=b'',
    )
    # 字典需先转换为json，后转换为byte
    str_1 = str(Transaction)
    b_deal = str_1.encode('UTF-8')

    # 发送交易
    conn.sendall(b_deal)

    data = []
    flag = 0

    while True:
        # 接受数据
        if flag == 5:
            break
        result = conn.recv(1024)
        data.append(result)
        #
        # # 输出数据
        # print('###')
        # print(result)
        flag = flag + 1

    s_rawTransaction = hexbytes.HexBytes(data[0])
    s_hash = hexbytes.HexBytes(data[1])
    s_r = int(data[2])
    s_s = int(data[3])
    s_v = int(data[4])

    s = SignedTransaction.make_signedTransaction(SignedTransaction, s_rawTransaction, s_hash, s_r, s_s, s_v)
    print(s)

    # 进行交易
    tx_hash = w3.eth.sendRawTransaction(s.rawTransaction)

    print('Deal Success!')
    # 关闭连接
    conn.close()
    server_receive.close()


if __name__ == '__main__':

    First_address = '0xf5e7d4Ac497af19cAF97d459048f8Efe5ac833BC'
    Second_address = '0x7E4BBD69250C1F6B21023c6a21A0F5ef836b4578'
    First_pw = 'ecf7868c95b4767e732091d0aad5203995399ce4739d20e075e8ec09765f3212'
    Second_pw = '740fffe4f5fdd194be7df8f823fbf2bc720af80def78e967ae32ea15a8d60a24'
    RPC_server = 'HTTP://127.0.0.1:7545'
    number = 1

    Server_Transaction(RPC_server,First_address,Second_address,number)