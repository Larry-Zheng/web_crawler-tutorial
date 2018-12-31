# -*- coding: cp936 -*- 
#coding=utf-8
import requests
import re

def gen_url(patt):
    x=0
    while 1:
        x+=1
        yield patt.format(x)
        
        
        
novel='http://www.jjwxc.net/onebook.php?novelid=3483838&chapterid={}'
f=open("test.txt",'a+')

for url in gen_url(novel):
    res=requests.get(url)
    
    #若遇到无法正常显示 can‘t  decode xxx by ...
    #查编码之后 编码方式为 莫民奇妙（比如土耳其语，我遇到的）
    #且编码可信度很低时
    #多半有字符在干扰编码 可以用errors参数忽略错误
    #这样做的代价是 bs和etree可能就无法对内容进行解析了
    #我们只能用re模块进行内容抓取
    
    res=res.content.decode('gb18030',errors='ignore')
    
    try:
        content=re.findall('(.*?)<br>',res)
        title=re.findall('<h2>(.*?)</h2>',res)
        title='标题：'+title[0]
        f.write(title)
        
        content[0]=content[0].strip()
        for c in content:
            if 'readsmall'in c :
                continue
            if '<div 'in c or 'stoneBanlance' in c:
                print ('done')
                f.write('\n\n---------------------------------------------------------------------------\n')
                break
            f.write('\n'+c)
       
    except:
        print ('finished！')
        
        break
        
f.close()       

