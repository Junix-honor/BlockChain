import commands
import os
import sys

def callsh(sourceaddr,destinaddr,value,host,port):
    value=value*1000000000000000000
    cmm='bash /root/WXtest0419/starter'+' '+sourceaddr+' '+destinaddr+' '+str(value)+' '+host+' '+port
    status,out=commands.getstatusoutput(cmm)
    print(out)
    loca=out.find('contract address:    0')
    ca=out[loca:loca+63]
    print(ca)
    addrstart=ca.find('0')
    contraddr=ca[addrstart:]
    #print(contraddr)
    return contraddr
#api callsh,format as above
