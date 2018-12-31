#coding=utf-8  
import requests
import chardet
from bs4 import BeautifulSoup

res=requests.get('https://jobs.51job.com/chengdu-gxq/105472062.html?s=01&t=0')
soup=BeautifulSoup(res.content,'html.parser',from_encoding='gb18030')
 
 

addr=soup.find_all('span',"bname")
print (addr[-1].text)
 
 
element = soup.find('span', text='上班地址：').parent
print (element.text)

