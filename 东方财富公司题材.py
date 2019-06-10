# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:39:12 2019

@author: dairongyi
"""

import time
import numpy as np
import pandas as pd
import datetime

import selenium
from selenium import webdriver
import sys


import re

options = webdriver.FirefoxOptions()
options.set_headless()

class East_money():
    def __init__(self):
        self.driver = webdriver.Firefox(options = options) #
        self.data_path = './out_data/'
        self.base_url = 'http://data.eastmoney.com/gstc/'
        
    def 获取公司(self):
        self.driver.get(self.base_url)
        
        column_name1 = []
        col_body1 = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[4]/div/div/div[2]/div/div/table/thead/tr/th')
        for i in range(0, len(col_body1)):
            col_name1 = col_body1[i].text
            col_name1 = col_name1.replace('\n', '')
            column_name1.append(col_name1)
            
        column_name2 = []
        col_body2 = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/table/thead/tr/th')
        for i in range(0, len(col_body2)):
            col_name2 = col_body2[i].text
            col_name2 = col_name2.replace('\n', '')
            column_name2.append(col_name2)
        
#        try:
#        page = self.driver.find_element_by_class_name('PageNav').find_elements_by_xpath('div/a')[-3].text
#        page_numbers = int(page)
#        print (page_numbers)    
        count = 1
        page_numbers = 5
        df_tot = pd.DataFrame()        

        # 获取数据
        while count <= page_numbers:
#            print('第' + str(count) + '页')
            
            body1 = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[4]/div/div/div[2]/div/div/table/tbody/tr')
            while len(body1) <3:
                print('加载中')
                time.sleep(10)
                body1 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[2]/div/table/tbody/tr')
            list_tot1 = []
            for i in range(0, len(body1)):
                i1_col = body1[i].find_elements_by_xpath('td')
                list1 = []
                for j in range(0, len(i1_col)):
                    if j != 5:
                        j1_col = i1_col[j].text
                        j1_col = j1_col.replace('\n', '')
                        list1.append(j1_col)
                    else:
                        j1_col = i1_col[j].find_element_by_class_name('popTxt').get_attribute('textContent')
                        j1_col = j1_col.replace('\n', '')
                       
                        list1.append(j1_col)
  
                list_tot1.append(list1)
            df1 = pd.DataFrame(list_tot1, columns = column_name1)
            
            body2 = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/table/tbody/tr')
            while len(body2) <3:
                print('加载中')
                time.sleep(10)
                body2 = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/div[2]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div/table/tbody/tr')
            list_tot2 = []
            for i in range(0, len(body2)):
                i2_col = body2[i].find_elements_by_xpath('td')
                list2 = []
                for j in range(0, len(i2_col)):
                    j2_col = i2_col[j].text
                    j2_col = j2_col.replace('\n', '')
                    list2.append(j2_col)
                list_tot2.append(list2)
            df2 = pd.DataFrame(list_tot2, columns = column_name2) 
            df = pd.concat([df1, df2], axis = 1)
#            print (df)
            
            try:
                # 翻页
                self.driver.find_element_by_class_name('PageNav').find_elements_by_xpath('div/a')[-2].click()
                count += 1
                time.sleep(1)
            except:
                pass

            df_tot = pd.concat([df_tot, df], axis = 0)
            df_tot = df_tot.reset_index(drop =True)

        return df_tot
            

if __name__ == '__main__':
    self = East_money()
    result = self.获取公司()
    print ('汇总')
    print (result)
        
    self.driver.quit()  # 关闭网页驱动