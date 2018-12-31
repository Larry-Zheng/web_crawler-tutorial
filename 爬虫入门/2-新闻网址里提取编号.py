import requests
import re
from bs4 import BeautifulSoup
newsurl='http://news.sina.com.cn/china/'
res=requests.get(newsurl)
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'lxml')
#print(soup.prettify())

header=soup.select('.news-item')#抓取class属性为news-item的标签

for x in header:
    #文章中已经说明
    #相应上下级关系是 .news-item>h2>a
    #所以我们抓取a标签前一定要判断 h2是否存在
    if len(x.select('h2'))>0:

        #由于返回的是存放一个元素列表
        #所以取出第一个元素
        #再取出其href属性内容 即网址
        link=x.select('a')[0]['href']

        
        #print(link)
        code=link.split('/')[-1].rstrip('.shtml')
        time=link.split('/')[-2]
        print ('时间：',time,'编号：',code)
        #法二
        #link2=re.search(r'doc-(.*).shtml',link)
        #print (link2.group(1))
