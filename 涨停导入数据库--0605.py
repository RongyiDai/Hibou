''''
作者非本人
上传在此用作今后学习
''''
import time
import numpy as np
import pandas as pd
import datetime

import selenium
from selenium import webdriver
import sys

sys.path.append('../sql_api')
import api_data

import re
# 不打开网页的方式
options = webdriver.FirefoxOptions()
options.set_headless()
import os
import json
from pymongo import MongoClient

sys.path.append('../sql_api')
import api_data

ip = '192.168.1.23'
port = 27017
hostA = "event_analysis"
passwordA = "123456"
database = 'event_analysis_db'

class Spider_mian(api_data.api_data):

    def __init__(self):
        api_data.api_data.__init__(self)
        self.date_stock_day = self.read_field('date_stock_day','2017-01-01')
        self.data_path = './out_data/'
       

    def login_mongodb(self,ip,port,hostA,passwdA,datebase):
        pass
        #建立MongoDB数据库连接
        client = MongoClient(ip,port)
        try:
            db = client['admin'] # 建立数据库的连接 # 设置的管理员用户，先要从admin管理员数据库走
            ##db.authenticate("read_admin", "read_admin") # 只读的管理员账户
            db.authenticate(hostA, passwdA) # 大权限管理员账户,权限认证
            db = client[datebase]
        except:
            db = client[datebase]
            db.authenticate(hostA, passwdA)
        return db
    
    
    def insert_data(self, tablename, db): #df
        colT = db[tablename]
        
        date_list = list(self.date_stock_day['date'])
        filename = os.listdir(self.data_path)
        
        sql_date = list(set(pd.DataFrame(list(colT.find({},{'date'})))['date']))
        

        for date in date_list:
            fileT = '股票涨停' + date + '.xlsx'
            if fileT not in filename:
                print(date + '无数据')
                continue
            else:
                pass
            dataT = pd.read_excel(self.data_path + fileT)
            dataT['date'] = date
            dataT = dataT.reset_index(drop=True)
            b = colT.insert_many(json.loads(dataT.T.to_json()).values())
    
#        out = pd.DataFrame(list(colT.find({'date':'2019-05-29'})))
        return b
            
if __name__ == "__main__":
    self = Spider_mian()
    db = self.login_mongodb(ip, port, hostA, passwordA, database)
    b = self.insert_data('test',db)
