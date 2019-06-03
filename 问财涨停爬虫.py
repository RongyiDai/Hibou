import time
import numpy as np
import pandas as pd
import datetime

import selenium
from selenium import webdriver



class Spider_mian():

    def __init__(self):

        self.base_url = {'问财涨停':'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=20190603涨停'}

        self.driver = webdriver.Firefox(options = options)
        self.data_path = './data/'



    #更新每日股票涨停
    def 更新每日股票涨停(self, date_str, way = 1):

        print ('股票涨停')
        page_numbers = 2
        count = 1
        df_tot = pd.DataFrame()
        self.driver.get(self.base_url['问财涨停'])

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
                for j in range(0, 4):
                    if j == 1:
                        pass
                    else:
                        strT0 = i1_col[j].text
                        list1.append(strT0)
                list_tot1.append(list1)
            col_name1 = ['序号', '股票代码', '股票简称']
            df1 = pd.DataFrame(list_tot1, columns = col_name1)
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
                for j in range(0, 15):
                    if j != 5:
                        strT1 =  i2_col[j].text
                        list2.append(strT1)
                    else:
                        pass
                        # T = i2_col[j].find_elements_by_xpath('div/a')
                        # strT1 = T[0].get_attribute('href')
                        # list2.append(strT1)
                list_tot2.append(list2)
            col_name2 = ['现价', '涨跌幅（%）', '涨停', '首次涨停时间', '最终涨停时间', '连续涨停天数', '涨停原因类别', '涨停封单量（股）', '涨停封单额（元）', '涨停封成比（%）', '涨停封流比', '涨停开板次数', 'a股流通市值', '上市天数（天）']
            df2 = pd.DataFrame(list_tot2, columns = col_name2)

            df = pd.concat([df1, df2], axis = 1)
            
            
            print(df)

            try:
                # 翻页
               # self.driver.find_element_by_class_name("next").find_elements_by_xpath("a").click()
                self.driver.find_element_by_class_name("next").click()
                count += 1
                time.sleep(4)
            except:
                logging.
                pass
            
            df_tot = pd.concat([df_tot, df], axis = 0)
            df_tot.reset_index(drop=True)
        print ('汇总')
        print (df_tot)
        return df_tot
            
if __name__ == "__main__":
    self = Spider_mian()

    date_str = '2019-06-03'

    way = 1
    df_tot = self.更新每日股票涨停(date_str)
    df_tot =  df_tot.reset_index(drop=True)
    df_tot.to_excel('aa.xlsx')

#    self.driver.quit()  # 关闭网页驱动