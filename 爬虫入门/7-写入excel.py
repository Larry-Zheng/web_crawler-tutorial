#coding=utf-8  
# -*- coding: cp936 -*- 
import requests
from bs4 import BeautifulSoup
import json
import re
import pandas
detailurl='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1516606412563' 

def getdetails(url):
    fetchdetail={}
    res1=requests.get(url)
    res1.encoding='utf-8'
    soup1=BeautifulSoup(res1.text,'html.parser')    
    if len(soup1.select('.show_author'))>0:
        fetchdetail['标题']=soup1.select('.main-title')[0].text.encode('utf-8')
        fetchdetail['时间']=soup1.select('.date')[0].text.encode('utf-8')
        authority=soup1.select('.show_author')[0].text.lstrip(u'责任编辑：')
        authority=authority.encode('utf-8')
        fetchdetail['编辑']=authority
        fetchdetail['链接']=url
    #print '时间:',timesource
    #print  '编辑',authority
    #print '标题:',head
    #print'内容：\n\t',article
    #print'链接:',newsurl
    #print'\n\n'
    return fetchdetail

def getlist(url,num): #从1到num页的所有新闻网址提取
    fetch=[]
    for i in range(1,num):
        allurl=url.format(i)
        res=requests.get(allurl)
        jd=json.loads( res.text.lstrip('  newsloadercallback(').rstrip(');') )
        for ent in jd[u'result'][u'data']:
            pagelink=ent[u'url'].encode('utf-8')
            fetch.append(getdetails(pagelink))
    return fetch  


print('爬取中...')
test=getlist(detailurl,3)
print('完成爬取，正在写入...')
df=pandas.DataFrame(test) 
try:
    df.to_excel('news.xlsx')
except:
    print('请先关闭相应表格文件！')
else:
    print('完成！')


