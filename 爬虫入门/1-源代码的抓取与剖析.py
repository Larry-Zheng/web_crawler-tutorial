import requests
from bs4 import BeautifulSoup

#获取源码
newsurl='http://news.sina.com.cn/china/'
res=requests.get(newsurl)
res.encoding='utf-8'#编码 否则会出现中文乱码
#print(res.text)  #打印内容看是否符合要求

#剖析器
soup=BeautifulSoup(res.text,'lxml')
print(soup.prettify()) #规范打印
