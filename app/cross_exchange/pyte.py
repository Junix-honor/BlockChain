import subprocess
import os
import sys
from web3 import Web3
import json

basedir = os.path.abspath(os.path.dirname(__file__))


def callsh(sourceaddr, destinaddr, value, host, port):
    # print(type(value))
    value = value * 1000000000000000000
    value = int(value)
    cmm = 'bash ' + os.path.join(basedir, 'WXtest0419/starter') + ' ' + sourceaddr + ' ' + destinaddr + ' ' + str(
        value) + ' ' + host + ' ' + str(port)
    # cmm = 'bash /root/WXtest0419/starter' + ' ' + sourceaddr + ' ' + destinaddr + ' ' + str(
    #     value) + ' ' + host + ' ' + str(port)
    print(cmm)
    subp = subprocess.Popen(cmm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = subp.communicate()
    print(out)
    out = str(out)
    loca = out.find('contract address:    0')
    ca = out[loca:loca + 63]
    print(ca)
    addrstart = ca.find('0')
    contraddr = ca[addrstart:]
    print(contraddr)
    print('')
    return contraddr
# api callsh,format as above
