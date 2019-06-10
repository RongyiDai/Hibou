# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:32:03 2019

@author: dairongyi
"""

import time
import numpy as np
import pandas as pd
import datetime
import selenium
from selenium import webdriver
import sys
import os
import json
from pymongo import MongoClient
import re

import 东方财富公司题材

class east_money_db(东方财富公司题材.East_money):
    def __init__(self):
        
        东方财富公司题材.East_money.__init__(self)
        
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
    
    def insert_data(self, tablename, db):
        colT = db[tablename]
        df = self.获取公司()
#        df = df.reset_index(drop=True)
        b = colT.insert_many(json.loads(df.T.to_json()).values()) 
        
if __name__ == '__main__':
    self = east_money_db()
    db = self.event_analysis_db
    tablename = '东方财富'
    self.insert_data(tablename, db)
    
    self.driver.quit()  # 关闭网页驱动
    
    