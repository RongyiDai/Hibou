# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:04:53 2019

@author: dairongyi
"""

import time
import numpy as np
import pandas as pd
from datetime import datetime
import selenium
from selenium import webdriver
import sys
import os
import json
from pymongo import MongoClient
import re

import 东方财富机构调研

class East_money_jgdy_db(东方财富机构调研.East_money_jgdy):
    def __init__(self):
        东方财富机构调研.East_money_jgdy.__init__(self)
        ip = '192.168.1.23'
        port = 27017
        hostA = "event_analysis"
        passwordA = "123456"
        database = 'event_analysis_db'
        self.event_analysis_db = self.login_mongodb(ip, port, hostA, passwordA, database)
        
    #登录数据库
    def login_mongodb(self,ip,port,hostA,passwdA,database):
        
        #建立MongoDB数据库连接
        client = MongoClient(ip,port)
        try:
            db = client['admin'] # 建立数据库的连接 # 设置的管理员用户，先要从admin管理员数据库走
            ##db.authenticate("read_admin", "read_admin") # 只读的管理员账户
            db.authenticate(hostA, passwdA) # 大权限管理员账户,权限认证
            db = client[database]
        except:
            db = client[database]
            db.authenticate(hostA, passwdA)
        return db
    
    def insert_data(self, tablename, df, db):
        colT = db[tablename]
#        df = self.获取机构调研()
        df = df.reset_index(drop=True)
        b = colT.insert_many(json.loads(df.T.to_json()).values()) 
        
    def get_date(self, tablename, db):
        colT = db[tablename]
        if tablename not in db.list_collection_names():
            datelist = []
        else:
            datelist = list(set(pd.DataFrame(list(colT.find({},{'公告日期'})))['公告日期']))
        return datelist
#    
    def update_table(self, tablename, db):
        colT = db[tablename]
        sqldate = self.get_date(tablename, db)
        sqldate.sort(key = lambda d: datetime.strptime(d, '%Y-%m-%d')) #数据库中已有的公告日期
        latest_date = sqldate[-1]
        oldest_date = sqldate[0]
        colT.delete_many({'公告日期':latest_date})
        df = self.获取机构调研(date_start, latest_date, oldest_date)
        
        self.insert_data(tablename,df, db)
#        date_list = list(self.获取机构调研()['公告日期']) #网页上第一页的公告日期
        
        
if __name__ == '__main__':
    self = East_money_jgdy_db()
    tablename = '机构调研'
    db = self.event_analysis_db
    date_start = '2019-06-12'
    self.update_table(tablename, db)    

    self.driver.quit()  # 关闭网页驱动