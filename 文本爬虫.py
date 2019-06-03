# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:37:07 2019

@author: guoqing
"""

import pandas as pd
import selenium
from selenium import webdriver

class Spider_mian():

    def __init__(self):

        self.base_url = {'新浪股票':'https://finance.sina.com.cn/stock/'}

        self.driver = webdriver.Firefox()
        self.data_path = './data/'
        
    def 要闻搜索(self, date_str, way = 1):
        
        print ('要闻')
        self.driver.get(self.base_url['新浪股票'])
#        body = self.driver.find_elements_by_xpath('/html/body/div[9]/div[2]/div[2]/div[1]/div/div[1]')
        body = self.driver.find_elemenets_by_xpaths('/html/body/div[9]/div[2]/div[2]/div[1]/div/div[1]/ul[1]/li')
        for i in range (0, len(body)):
            i1_col = body1[i].find_elements_by_xpath('a')
