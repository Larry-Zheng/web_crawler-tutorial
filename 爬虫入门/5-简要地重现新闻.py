import requests
from bs4 import BeautifulSoup

##########################
#获取源码
newsurl='http://news.sina.com.cn/china/'
res=requests.get(newsurl)
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'lxml')
#######################

header=soup.select('.news-item')
for x in header[:6]: #不取过多新闻 取前6则示意即可
    if len(x.select('h2'))>0:
        link=x.select('a')[0]['href']
        reports=requests.get(link)
        reports.encoding='utf-8'
        soup1=BeautifulSoup(reports.text,'lxml') #取出链接 并获取子页面源码
        
        if soup1.select('.main-title'):
            head=soup1.select('.main-title')[0].text
            timesource=soup1.select('.date')[0].text
            content=soup1.select('.article p')
            article='\n\t'.join(p.text for p in content[:-1])
            authority=soup1.select('.show_author')[0].text.lstrip('责任编辑:')
            
            print ('时间:',timesource)
            print  ('编辑',authority)
            print ('标题:',head)
            print('内容：\n\t',article)
            print('链接:',link)
            print('\n\n#####################################################')
            
            
