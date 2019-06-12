# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:37:26 2019

@author: dairongyi
"""

import time
import datetime
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
import sys

options = webdriver.FirefoxOptions()
options.set_headless()

class East_money_jgdy():
    def __init__(self):
        self.driver = webdriver.Firefox() #options = options
        self.data_path = './out_data/'
        self.base_url = 'http://data.eastmoney.com/jgdy/tj.html'
    
        
    def 获取机构调研(self, date_start, latest_date, oldest_date): 
        self.driver.get(self.base_url)
        
        
        column_name = []
        col_body = self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div[4]/table/thead/tr/th')
        for i in range(0, len(col_body)):
            col_name = col_body[i].text
            column_name.append(col_name)
            
        count = 1
        page = self.driver.find_element_by_class_name('PageNav').find_elements_by_xpath('div/a')[-3].text
        page_numbers = int(page)

#        page_numbers = 2
        df_tot = pd.DataFrame()
        
        while count <= page_numbers:
            print ('Page' + str(count))
            body = self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div[4]/table/tbody/tr')
            while len(body) <3:
                print('加载中')
                time.sleep(15)
                body = self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/div[4]/table/tbody/tr')
            
            list_i = []
            for i in range(0, len(body)):
                i_col = body[i].find_elements_by_xpath('td')
                list_j = []
                for j in range(0, len(i_col)):
                    if j in range(7, 10):
                        try:
                            j_col = i_col[j].find_element_by_xpath('span').get_attribute('title')
                            list_j.append(j_col)
                        except:
                            list_j.append('-')
                    elif j == 11:
                        j_col = i_col[j].text.replace('/', '-')
                        year = i_col[j - 1].text[:4]
                        j_col = year + '-' + j_col
                        list_j.append(j_col)
                    else:
                        j_col = i_col[j].text
                        list_j.append(j_col)
                list_i.append(list_j)
            
            df = pd.DataFrame(list_i, columns = column_name)
            df_tot = pd.concat([df_tot, df], axis = 0)
            df_tot = df_tot.reset_index(drop = True)
            
            if len(df_tot[df_tot['公告日期']<date_start]):
                
                if date_start < oldest_date:
                    df_tot = df_tot[(df_tot['公告日期'] >= date_start) & (df_tot['公告日期'] < oldest_date) | (df_tot['公告日期'] >= latest_date ) ] #(
                    break
                else:
                    df_tot = df_tot[df_tot['公告日期'] >= latest_date] 
                    break

            try:
                self.driver.find_element_by_class_name('PageNav').find_elements_by_xpath('div/a')[-2].click()
                count += 1
                time.sleep(7)
            except:
                pass

        
        return df_tot
        
            
            
if __name__ == '__main__':
    self = East_money_jgdy()
#    date_start = '2019-06-05'
#    latest_date = '2019-06-10'
#    oldest_date = '2019-06-06'
    result = self.获取机构调研(date_start, latest_date, oldest_date)
    print ('Sum')
    print (result)
    
    self.driver.quit()