#!/usr/bin/env python
#coding:utf8
import ansible.runner

def getVal(data,user,pwd):
    runner = ansible.runner.Runner(
        remote_user = user,
        remote_pass = pwd,
        module_name = 'setup',
        host_list = ['{}'.format(data)],
        #become = True
        )

    data = runner.run()
    l = []
    for ip,val in data['contacted'].items():
        hostName = val['ansible_facts']['ansible_nodename']
        versions = version = val['ansible_facts']['ansible_distribution_version']
        l = [hostName.encode('utf-8'),versions.encode('utf-8')]
    return l

if __name__ == '__main__':
    data = runner.run()
    for ip,val in data['contacted'].items():
        hostName = val['ansible_facts']['ansible_nodename']
        version = val['ansible_facts']['ansible_distribution_version']
        print ip,hostName,version
