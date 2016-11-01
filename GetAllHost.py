#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#

from pyVim.connect import SmartConnect, Disconnect

import atexit
import ssl
import ConfigParser
from mysql import insert
from gethostname import getVal
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def VmInfo(vm,user,pwd,depth=1):
    maxdepth = 10
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            VmInfo(c,user,pwd, depth+1)
        return
    disk = ''
    vm_hardware = vm.config.hardware
    for each_vm_hardware in vm_hardware.device:
        if (each_vm_hardware.key >= 2000) and (each_vm_hardware.key < 3000):
            disk += str(each_vm_hardware.capacityInKB/1024/1024) + 'GB  '

    summary = vm.summary
    vmname = summary.config.name
    mem = summary.config.memorySizeMB
    cpu = summary.config.numCpu
    state = summary.runtime.powerState
    ip = summary.guest.ipAddress
    uuid = summary.config.uuid
    if ip is not None:
        val = getVal(ip,user,pwd)
        if val:
            if user == 'zhangjun13':
                li = [ip,val[0],mem,cpu,disk,val[1],1,state,vmname,uuid]
                print li
                insert(li)
            else:
                li = [ip,val[0],mem,cpu,disk,val[1],0,state,vmname,uuid]
                print li
                insert(li)
        else:
            li = [ip,'windows',mem,cpu,disk,'windows',0,state,vmname,uuid]
            print li
            insert(li)

def main(host,name,key,user,pwd):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=host,
                      user=name,
                      pwd=key,
                      port=443,
                      sslContext=context)
    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for vm in vmList:
                VmInfo(vm,user,pwd)

    return 'ok'

# Start program
if __name__ == "__main__":
   #connect('10.101.20.113','zhangjun13@vsphere.local','zuche@123')

    conf = ConfigParser.ConfigParser()
    conf.read('esxi.conf')
    dic = dict(conf.items('test'))
    main(dic['host'],dic['name'],dic['key'],dic['user'],dic['pass'])
