# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 13:59:55 2017

說明：爬取PTT 資料，可根據選取的版面、資料筆數爬取資料

@author: Jo_Lin
"""
import requests
import re                         #正規表示式的函式存在的包
from bs4 import BeautifulSoup
#import json

#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()  #去除requests發生的warring

boardName=input("請輸入您想蒐集的板名(例如:Japan_Travel):")
dataNum=input("請輸入想蒐集的資料數量")

count=1;  #紀錄資料筆數

#處理懶得輸入的時候
if dataNum is "":
    dataNum=10
if boardName is "":
    boardName="Japan_Travel"

url_path="https://www.ptt.cc/bbs/"+boardName+"/index.html"


#獲取最後一頁的頁數
def getTheLastPage(l_url_path):
    res = requests.get(l_url_path, verify=False)
    first_page = re.search(r'index(\d+).html">&lsaquo; 上頁', res.text).group(1)
    total_page = int(first_page)+1
    return(total_page)


list_spam=[]
#取得頁面的內容
def getContent(l_url_path):
        
        global count,dataNum,list_spam   #解決count+=1 會發生的問題，將count變成global的變數     

        sTitle=""
        sAuthor=""        
        pagehtml = requests.get(l_url_path, verify=False)
        sp=BeautifulSoup(pagehtml.text, 'html.parser')        
        item=sp.select(".r-ent")   #找到e-shopping文章
         
        for article in item :
            sTitle=article.select(".title")[0].text.strip()#strip()去除特殊字
#            print(str(count)+"."+str(ignoreStr(sTitle)))
            if(ignoreStr(sTitle)):  #判斷是否為已刪除的文章，假如是就不要記錄
                sAuthor=article.select(".author")[0].text
                
                spam_Data ={"title":sTitle,'Author':sAuthor}  #建立儲存資料的List
                spamInfo={}
                spamInfo['ID']=count
                spamInfo['Data']=spam_Data
                print(str(spamInfo))
                list_spam.append(spamInfo)
                count += 1
                if(count > int(dataNum)):
                    break
            else:
                continue

#ignore 字串
def ignoreStr(l_sTitle):
    match=False
    str_ignore=["刪除","處分","Fw","Re","已售出","已送出","空白文","禁止讓售","公告"]
    for cignore in str_ignore:
         if(cignore in l_sTitle):
             match=False
             break;
         else:
            match=True            
    return match

#寫入檔案
def createFile(wstr):
    fileName=boardName+".txt"
#    f = open('PTT_Japan.txt', 'a', encoding = 'UTF-8') 
    f = open(fileName, 'a', encoding = 'UTF-8') 
    f.write(wstr)
    f.write("\r\n")
    f.close()         


#================ 主程式 start====================

getPageCount=1;   #紀錄目前的頁數 
 
totalPage=getTheLastPage(url_path)  #取得總頁數
print("Pages:",totalPage)  



while(count < int(dataNum)):
    url_path="https://www.ptt.cc/bbs/"+boardName+"/index"+ str(totalPage) +".html"
    contentInfo=getContent(url_path)
    totalPage -= 1
print("========================")   
print(list_spam)

#createFile(spam)e
#for CI in contentInfo.values():
#            print (CI)
#================ 主程式 End ====================
        

