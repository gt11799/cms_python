#!/usr/bin/env Python

import os
import sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, ".."))
import traceback
from collections import OrderedDict
from settings import EXEC_PATH,REMAIN_MEM,INTERVEN,LOG_FILE
import re
import os
import subprocess
import shlex
import time
import logging

logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG)
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def exec_mem():
    while 1:
        mem=meminfo()
        mem['MemFree']=re.sub(r' ','',mem['MemFree'])
        pattern=r'(\d+\d)'
        match=re.search(pattern, mem['MemFree'])
        if not match:
            mem['MemFree']=0
        else:
            print "ddddddddddddd"
            print match.group(1)
            mem['MemFree']=float(match.group(1))
    
    
        if mem['MemFree'] <REMAIN_MEM:
            
            
            args = shlex.split(EXEC_PATH)
            
            try:
                subprocess.check_output(args,shell=True)
            except subprocess.CalledProcessError as callerr:
                
                logging.info("ERROR :%s" %callerr.returncode)
                logging.info("ERROR :%s" %callerr)     
                 
        time.sleep(float(INTERVEN))        
if __name__=='__main__':
    #print(meminfo())
    
    

    exec_mem()