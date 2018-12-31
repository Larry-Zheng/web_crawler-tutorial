#coding=utf-8
import requests
import chardet
from bs4 import BeautifulSoup
import time
def info(url):
    res1=requests.get(url)
    soup=BeautifulSoup(res1.content,'html.parser',from_encoding='gb18030')#!!content是通过bit读出的是str对于网页不存在编码时使用;建议用如述编码容错
    try:
        name=soup.select('h1')[0].text
    except:
        print('直招链接：%s'%(url))
        return

    print ('职位：',name)
    treatment=soup.select('.t2 span')
    treat=[]
    basic=soup.find_all('strong')
    treat.append(basic[1].text)
    for t in treatment:
        treat.append(t.text) 
    treat=('、').join(treat)
    print ('待遇:',treat)
    addr= soup.find('span', text='上班地址：').parent#text定向查找
    print (addr.text)
    info=soup.find('div',"bmsg job_msg inbox")#select 出现不妥时尝试findall 
    try:
        info.select('.mt10')[0].decompose()     
    except:
        pass
    try:
        info.select('.share')[0].decompose()#注意我们find和select的方法所返回的类型不同，对于tag我们可以对不要的tag删除
    except:
        pass
   
    print ('描述：\n\t',info.get_text('\n\t','br/'))#！！#重要的去除br方法
    intro=soup.find('div',"tmsg inbox")
    print ('公司介绍：\n\t',intro.get_text('\n\t','br/'))
    title=soup.find('p',"msg ltype")
    temp=title.text .replace('\t','').replace(' ','').strip().split('|')
    intro=(temp[0].strip()+u'、'+temp[1].strip())
    print ('公司规模:',intro)
    print ('公司性质:',temp[-1].strip())
    print ('####################################################')


res=requests.get('http://search.51job.com/list/060000,000000,0000,00,9,99,%2520,2,1.html')
soup=BeautifulSoup(res.content,'html.parser')
jlist=soup.select('#resultList')
content=jlist[0].find_all('div',"el")
urls=[]
for detail in content[1:]:
    url=detail.select('a')[0]['href'].encode('utf-8')
    urls.append(url)


for joburl in urls:
 
    info(joburl)
   
    
    time.sleep(1)

