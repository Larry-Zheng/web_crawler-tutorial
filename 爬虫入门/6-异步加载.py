
import requests
from bs4 import BeautifulSoup
import json

detailurl='http://api.roll.news.sina.com.cn/zt_list\
?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl\
||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22\
&tag=1&format=json&page={}&callback=newsloadercallback&_=1516606412563'#待访问的json文件


def getlink(url,num): #从1到num页的所有新闻网址提取
    fetch=[]    
    for i in range(1,num):

        #format是一个格式化函数
        #比如在这里 将数字i传入字符串里
        #更多讲解 详见 http://www.runoob.com/python/att-string-format.html
        allurl=url.format(i)
        res=requests.get(allurl)
        res=res.content.decode('utf-8',errors='ignore')
   
        
        
        #json.loads的作用其实就是讲字符串形式的字典 转换为真正的字典
        #这里res.text返回的字典内容 包覆在newsloadercallback()里
        #所以调用 lstrip 和 rstrip 将无关信息去掉
        jd=json.loads( res.lstrip('  newsloadercallback(').rstrip(');') )
        for ent in jd[u'result'][u'data']:
            fetch.append(ent[u'url'])   
    return fetch


def getdetails(url): #根据getlink函数提出来的网址抓取具体信息
    for newsurl in url:
        #######获取源码
        res1=requests.get(newsurl)
        soup1=BeautifulSoup(res1.content.decode('utf-8',errors='ignore')\
                            ,'lxml')
        #搜索元素
        head=soup1.select('.main-title')[0].text
        timesource=soup1.select('.date')[0].text
        contents=soup1.select('.article p')
        article='\n\t'.join(p.text for p in contents[:-1])
        authority=soup1.select('.show_author')[0].text.lstrip('责任编辑:')
        #打印
        print ('时间:',timesource)
        print  ('编辑',authority)
        print ('标题:',head)
        
        #这里存在一个tk无法显示的编码
        #我们切换到jupyter后便可以显示
        try:
            print('内容：\n\t',article)
        except:
            print('存在未知错误编码！')
            print(res1.text)
        print('链接:',newsurl)
        print('\n\n')



testurl=getlink(detailurl,2)
getdetails(testurl) 
 
