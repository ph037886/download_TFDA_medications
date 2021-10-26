# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:09:55 2021
Python 3.7.8
"""
#這隻code我沒有很有信心他一定能動，因為這個在我整理的時候就已經是改到亂的，當年也不會用git，沒有很確定是不是能運作

import pandas as pd # 引用套件並縮寫為 pd  
import urllib
import urllib.request
df = pd.read_csv('files/out.csv')
df=df[~df['備註'].str.contains('健保碼錯誤')] #這段篩選我沒有很確定，我自己實際做的時候是在excel做篩選
i=0
while i<len(df):
    url=pd.iat[i,4]
    #url=str("https://info.fda.gov.tw/MLMS/H0001D3.aspx?LicId=" + str(df.iat[i,1]))
    urllib.request.urlretrieve(url, "files/download/"+df.iat[i,1]+".pdf") #這邊注意，如果仿單不是pdf檔，出來的會是錯誤的
    i+=1
print('finish')
