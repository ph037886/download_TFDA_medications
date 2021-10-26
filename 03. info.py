# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 19:03:50 2021
Python 3.7.8
"""

import pandas as pd # 引用套件並縮寫為 pd  
from selenium import webdriver #引用網頁程式
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#引入我的資料庫
df = pd.read_excel(r'files\name_list.csv')
#新增一列下載網址欄位
df["連結代碼"]=""
df["許可證字號"]=""
df["適應症"]=""
df["劑型"]=""
df["備註"]=""
#網頁執行
driver = webdriver.Firefox(executable_path='D:/Python/lable/geckodriver.exe') #開啟firefox
driver.get("https://www.nhi.gov.tw/QueryN/Query1.aspx") #前往這個網址
i=0
while i<len(df):
    driver.get("https://www.nhi.gov.tw/QueryN/Query1.aspx") #前往這個網址
    search_input = driver.find_element_by_name("ctl00$ContentPlaceHolder1$tbxQ1ID")#健保碼欄位
    search_input.send_keys(df.iat[i,1]) 
    start_search_btn = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSubmit")
    start_search_btn.click()
    #如果健保碼錯誤查無資料則跳過，記錄下來
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()
        df.iloc[i,9]="健保碼錯誤"
        i+=1
    except TimeoutException:
        link_value=driver.find_element_by_name("ctl00$ContentPlaceHolder1$gvQuery1Data$ctl02$hid_doh_id")
        df.iloc[i,2]=link_value.get_attribute("value") #取得連結代碼
        driver.get("https://info.fda.gov.tw/MLMS/H0001D.aspx?Type=Lic&LicId="+df.iloc[i,2])    
        df.iloc[i,3]=driver.find_element_by_id("lblLicName").text
        df.iloc[i,4]=driver.find_element_by_id("lblIndiCat").text
        df.iloc[i,5]=driver.find_element_by_id("lblDoesName").text
        df.iloc[i,5]=driver.find_element_by_id("lblDoesName").text
    print(str(i)+"/"+str(len(df)))
    i+=1
driver.quit()
df.to_excel(r'files/藥品資料.xlsx',index=False)
