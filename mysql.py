#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-28 14:30:42
# @Author  : zhangjun
# @Link    : http://example.org
# @Version : 0.1

import MySQLdb
import ConfigParser

conf = ConfigParser.ConfigParser()
conf.read('esxi.conf')
dic = dict(conf.items('mysql'))

conn = MySQLdb.connect(host='xxx',user='xxx',passwd='xxx',db='webapps',charset='utf8')
cur = conn.cursor()

def insert(data):
    print data
    sql = "insert into webapp_cmdb (hostIp,hostName,mem,cpu,disk,versions,isroot,state,vmname,uuid) values('%s','%s','%d','%s','%s','%s','%s','%s','%s','%s')" %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
    print sql
    cur.execute(sql)
