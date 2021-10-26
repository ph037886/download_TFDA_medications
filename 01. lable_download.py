# -*- coding: utf-8 -*-
#Python 3.7.8

import pandas as pd
from selenium import webdriver #引用網頁程式
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#引入我的資料庫
df = pd.read_csv('files/name_list.csv')
#新增一列下載網址欄位
df["連結代碼"]=""
df["下載網址"]=""
df["備註"]=""
#網頁執行
driver = webdriver.Firefox(executable_path='files/geckodriver.exe') #開啟firefox
driver.get("https://www.nhi.gov.tw/QueryN/Query1.aspx") #前往這個網址
i=0
while i<len(df):
    driver.get("https://www.nhi.gov.tw/QueryN/Query1.aspx") #前往這個網址
    search_input = driver.find_element_by_name("ctl00$ContentPlaceHolder1$tbxQ1ID")
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
        df.iloc[i,4]="健保碼錯誤"
        df.iloc[i,3]=""
        i+=1
    except TimeoutException:
        link_value=driver.find_element_by_name("ctl00$ContentPlaceHolder1$gvQuery1Data$ctl02$hid_doh_id")
        link_index=link_value.get_attribute("value")
        df.iloc[i,2]=link_index
        driver.get("https://info.fda.gov.tw/MLMS/H0001D3.aspx?LicId="+link_index)
    # 取得下載連結
        lnks=driver.find_elements_by_tag_name("a")
        link=[]
        for lnk in lnks:
            link+=[lnk.get_attribute('href')]
        #如果沒有仿單資料記錄下來
        if len(link)<2:
            df.iloc[i,4]="沒有仿單資料"
            df.iloc[i,3]=""
            i+=1
        else:
            df.iloc[i,3]=link[1]
            i+=1
driver.quit()
df.to_csv('files/out.csv')
