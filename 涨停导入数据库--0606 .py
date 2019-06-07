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


sys.path.append('../sql_api')
import api_data
import pachong


# 不打开网页的方式
options = webdriver.FirefoxOptions()
options.set_headless()


class pachong_db(pachong.Spider_mian,api_data.api_data):

    def __init__(self):
        api_data.api_data.__init__(self)
        pachong.Spider_mian.__init__(self)
        
        self.date_stock_day = self.read_field('date_stock_day','2017-01-01')
        self.data_path = './out_data/'
        
        ip = '192.168.1.23'
        port = 27017
        hostA = "event_analysis"
        passwordA = "123456"
        database = 'event_analysis_db'
        self.event_analysis_db = self.login_mongodb(ip, port, hostA, passwordA, database)
       
    #登录数据库
    def login_mongodb(self,ip,port,hostA,passwdA,database):
        pass
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
    
     #插入数据   
    def insert_data(self, tablename, df,db): #df
        colT = db[tablename]
        df = df.reset_index(drop=True)
        b = colT.insert_many(json.loads(df.T.to_json()).values()) 
        
    #获取集合（表格）中已有的日期
    def get_date(self, tablename, db):
        colT = db[tablename]
        if tablename not in db.list_collection_names(): #判断数据库中是否有该表
            datelist = []
        else:
            datelist = list(set(pd.DataFrame(list(colT.find({},{'date'})))['date']))
        return datelist
    
    def update_table(self,tablename, db):
        sqldate = self.get_date(tablename, db)
        date_list = list(self.date_stock_day['date'])
        date_list = list(set(date_list)-set(sqldate))
        for date in date_list:
            print('更新：'+tablename+'_'+date)
            df = self.更新每日股票涨停(date, tablename)
            self.insert_data(tablename, df,db)

            
if __name__ == "__main__":
    self = pachong_db()
    db = self.event_analysis_db
    tablename = '跌停'
    tablelist = ['涨停','跌停']
    for table in tablelist:
        try:   
            self.update_table(tablename,db)
        except:
            pass



