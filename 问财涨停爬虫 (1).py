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

class Spider_mian(api_data.api_data):

    def __init__(self):
        api_data.api_data.__init__(self)
        
        self.date_stock_day = self.read_field('date_stock_day','2017-01-01')

#        self.base_url = {'问财涨停':'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w='+ date_str +'涨停'}

        self.driver = webdriver.Firefox(options = options) #
        
        self.data_path = './out_data/'

#获取URL
    def get_url(self,date_str):
        self.base_url = {'问财股票涨停':'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w='+ date_str +'涨停',
                         '问财综合评分':'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=' + date_str + '综合评分&queryarea='}
        
            
#        self.column = {'问财涨停': ['序号', '股票代码', '股票简称', '现价', '涨跌幅（%）', '涨停', '首次涨停时间', '最终涨停时间', '连续涨停天数', '涨停原因类别', '涨停封单量（股）', '涨停封单额（元）', '涨停封成比（%）', '涨停封流比', '涨停开板次数', 'a股流通市值', '上市天数（天）'],
#                       '问财综合评分：'}

    #更新每日股票涨停
    def 更新每日股票涨停(self, date_str, urlname, way = 1):
        self.get_url(date_str)
        url = self.base_url[urlname]
        
#        url = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w='+date_str+'涨停'


#        self.driver.get(self.base_url['问财涨停'])
        self.driver.get(url)
        
#        获取列名
        column_name1 = []
        col_body1 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[2]/div/div/ul/li')

#        col_body1 = self.driver.find_element_by_class_name('clearfix static_table thead_table static_thead_table')
        
#        print (len(col_body1))
        for i in range (0, len(col_body1)):
            col_name1 = col_body1[i].text
            column_name1.append(col_name1)
           
        
        column_name2 = []
        col_body2 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li')
        print (len(col_body2))
        for i in range (0, len(col_body2)):
                col_name2 = col_body2[i].get_attribute('big_title')
                print (col_name2)
                column_name2.append(col_name2)
                
        
        
#        column_name3 = []
#        col_body3 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]/ul/li/div')    
#        for i in range (0, 7):
#                col_name3 = col_body3[i].text
#                column_name3.append(col_name3)
#        print (column_name3)
        
#        获取页数
        page = self.driver.find_element_by_class_name('total').text
        print (date_str + '%s'% urlname + page)
#        dir(self.driver)
        page_numbers = int(''.join(re.findall(r'[0-9]', page)))
        count = 1
        df_tot = pd.DataFrame()        
        

#        获取数据
        while count <= page_numbers:
            print ('第' + str(count) + '页')

            body1 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[2]/div/table/tbody/tr')
            while len(body1) <3:
                print ('股票加载中')
                time.sleep(10)
                body1 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[2]/div/table/tbody/tr')
            list_tot1 = []
            for i in range(0, len(body1)):
                #i0 = body1[i]
                i1_col = body1[i].find_elements_by_xpath('td')
                list1 = []
                for j in range(0, len(i1_col)-1):
                    strT0 = i1_col[j].text
                    list1.append(strT0)
                list_tot1.append(list1)
#            col_name1 = ['序号', '股票代码', '股票简称']
            df1 = pd.DataFrame(list_tot1, columns = column_name1) 
            #print (df1)


            body2 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[2]/table/tbody/tr')
            while len(body1) < 3:
                print ('股票加载中')
                time.sleep(10)
                body2 = self.driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[5]/div/div[6]/div[8]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[2]/table/tbody/tr')
            list_tot2 = []
            for i in range(0, len(body2)):
                #i1 = body2[i]
                i2_col = body2[i].find_elements_by_xpath('td')
                list2 = []
                for j in range(0, len(i2_col)-1):
#                    if j != 5:
                    strT1 =  i2_col[j].text
                    list2.append(strT1)
#                    else:
#                        pass
                        # T = i2_col[j].find_elements_by_xpath('div/a')
                        # strT1 = T[0].get_attribute('href')
                        # list2.append(strT1)
                list_tot2.append(list2)
#            col_name2 = ['现价', '涨跌幅（%）', '涨停', '首次涨停时间', '最终涨停时间', '连续涨停天数', '涨停原因类别', '涨停封单量（股）', '涨停封单额（元）', '涨停封成比（%）', '涨停封流比', '涨停开板次数', 'a股流通市值', '上市天数（天）']
            df2 = pd.DataFrame(list_tot2, columns = column_name2) #, columns = col_name2

            df = pd.concat([df1, df2], axis = 1)
            
            
            print(df)

            try:
                # 翻页
               # self.driver.find_element_by_class_name("next").find_elements_by_xpath("a").click()
                self.driver.find_element_by_class_name("next").click()
                count += 1
                time.sleep(4)
            except:
                
                pass
            
            df_tot = pd.concat([df_tot, df], axis = 0)
            df_tot.reset_index(drop=True)
          #print ('汇总')
        # print (df_tot)
        return df_tot
            
if __name__ == "__main__":
    self = Spider_mian()

#    date_str = '2019-06-01'
#    fmt = '%Y-%m-%d'
    urlname = '问财综合评分'
    date_list = list(self.date_stock_day['date'])[-1:]
#    
#    for date_str in date_list:
#        way = 1
#        df_tot = self.更新每日股票涨停(date_str, urlname)
#        df_tot =  df_tot.reset_index(drop=True)
#        df_tot.to_excel(self.data_path + '%s' %urlname +'%s.xlsx' % date_str)
#        
#
#
#    self.driver.quit()  # 关闭网页驱动