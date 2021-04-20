#  get fields from fore stage
#  call shell scripts to make contract files, compile, build and push to chain
#  able to be multi-called, parrallel

## py file


#shell need         contract hash
#                   source(local) account hash
                                    #key of it
                   #destina(oppo) account hash
                                    #key of it
                                    
## only the origin caller trigger the fx---search partner(who the origin caller to finish the procudure with)
#import valuelist

import os
import sys

def calexchange( sourcechain, aimchain, value):
    float valueX=value
    #rate from imported valuelist
    #rate=$perCreditOf1/$perCreditOf2
    #valueX=value*rate
    return valueX

def searchPartner(string sourcechain,string aimchain,float valueX):
    #select userid from ACCOUNTTABLE where chain=aimchain and balance>valueX Order by balance ASC;
    #call the user found
    


float valueX=calexchange(~,~,originvalue)
searchPartner(chain1,chain2,valueX)
os.popen("shell starter")# shell needs some para
    # get feedback from shell scripts starter
string state
if state=="Unlocked2":
    os.popen("shell ender")#shell needs some para
    else:
        sys.exit()

