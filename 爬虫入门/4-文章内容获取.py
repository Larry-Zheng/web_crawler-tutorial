# *-* coding:utf-8 *-*

####################################
#获取源码
import requests
from bs4 import BeautifulSoup
from datetime import datetime
newsurl='http://news.sina.com.cn/c/nd/2018-01-21/doc-ifyquptv8361037.shtml'
res=requests.get(newsurl)
res.encoding='utf-8'
#print(res.text)
##################################################


soup=BeautifulSoup(res.text,'lxml')
print (soup.select('.main-title')[0].text)#打印标题标题


'''
#print type(timesource)
#timesource=timesource.encode('utf-8')#非常关键，让转换函数识别
#print type(timesource)
#timesource
#f=open("E:/test.txt",'w')
#f.write(timesource)
#f.close()#测试成功utf8可以向外转为中文

'''
##############
#这一部分 调用datetime的函数
#将时间统一为 xxxx-xx-xx 的形式
#这里用re模块也是可以的 不过会稍微麻烦一点

#更多请参考 https://blog.csdn.net/ljh0302/article/details/54882750
# 和 https://blog.csdn.net/huangpin815/article/details/70495906
timesource=soup.select('.date')[0].text #获取时间
dt=datetime.strptime(timesource,'%Y年%m月%d日 %H:%M')#处理时间
strtime=dt.strftime('%Y-%m-%d')
print (strtime)#打印时间
##################

content=soup.select('#article > p') #获取内容
'''
#法1
article=[]
for p in content[:-1]:
    article.append(p.text.strip()) 
article='\n\t'.join(article)
print (article)
'''
#法2
article='\n\t'.join(p.text.strip() for p in content[:-1]) #列表推导式
print (article)
