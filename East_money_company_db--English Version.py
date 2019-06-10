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

import East_money_company

class east_money_db(East_money_company.East_money):
    def __init__(self):
        
        East_money_company.East_money.__init__(self)
        
        ip = '192.168.1.23'
        port = 27017
        hostA = "event_analysis"
        passwordA = "123456"
        database = 'event_analysis_db'
        self.event_analysis_db = self.login_mongodb(ip, port, hostA, passwordA, database)
        
    #log onto database
    def login_mongodb(self,ip,port,hostA,passwdA,database):
        
        # connect to MongoDB
        client = MongoClient(ip,port)
        try:
            db = client['admin'] 
            ##db.authenticate("read_admin", "read_admin") # read only account
            db.authenticate(hostA, passwdA) # authenticate manager user account
            db = client[database]
        except:
            db = client[database]
            db.authenticate(hostA, passwdA)
        return db
    
    # insert data of companies from east_money.com to database
    def insert_data(self, tablename, db):
        colT = db[tablename]
        df = self.get_company()
#        df = df.reset_index(drop=True)
        b = colT.insert_many(json.loads(df.T.to_json()).values()) 
        
if __name__ == '__main__':
    self = east_money_db()
    db = self.event_analysis_db
    tablename = '东方财富'
    self.insert_data(tablename, db)
    
    self.driver.quit()  # turn off webdriver
    
    