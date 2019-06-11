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

import East_money_company_research

class East_money_jgdy_db(East_money_company_research.East_money_jgdy):
    def __init__(self):
        East_money_company_research.East_money_jgdy.__init__(self)
        ip = '192.168.1.23'
        port = 27017
        hostA = "event_analysis"
        passwordA = "123456"
        database = 'event_analysis_db'
        self.event_analysis_db = self.login_mongodb(ip, port, hostA, passwordA, database)
        
    #log onto database
    def login_mongodb(self,ip,port,hostA,passwdA,database):
        
        #connect to MongoDB
        client = MongoClient(ip,port)
        try:
            db = client['admin'] 

            db.authenticate(hostA, passwdA) # authenticate manager user account
            db = client[database]
        except:
            db = client[database]
            db.authenticate(hostA, passwdA)
        return db
    
    def insert_data(self, tablename, df, db):
        colT = db[tablename]

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
        sqldate.sort(key = lambda d: datetime.strptime(d, '%Y-%m-%d')) #date in databse
        latest_date = sqldate[-1] #latest date in database
        colT.delete_many({'公告日期':latest_date})
        df = self.get_company_research(latest_date)
        
        self.insert_data(tablename,df, db)
#        date_list = list(self.get_company_research()['公告日期']) #网页上第一页的公告日期

        
        
if __name__ == '__main__':
    self = East_money_jgdy_db()
    tablename = '机构调研' #table name is 'company research'
    db = self.event_analysis_db
    self.update_table(tablename, db)

    self.driver.quit()  # 关闭网页驱动