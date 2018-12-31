import requests
from lxml import etree
import csv
import time

def normal(url,csvf):
    writer=csv.writer(csvf)

    print('executing...',end='')
    ####################################################
    res=requests.get(url)
    tree=etree.HTML(res.text)
    name=tree.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()')
    name=name[0] 
    ########################职位名

    ######################基本工资和福利
    bonus=tree.xpath('/html/body/div[5]/div[1]/div[1]/div[1]/span/text()') 
    basic=tree.xpath('/html/body/div[6]/div[1]/ul/li[1]/strong/text()')
    salary=[]
    salary.append(basic[0][:-1])
    salary.extend(bonus)
    salary=('、').join(salary) 
    
    ##############################地址
    addr=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/h2/text()')
    addr=addr[0].strip() 
   
    #########################具体描述
    dscr=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/p')

    #####################################公司名
    cname=tree.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()')
    cname=cname[0] 
    
    ##########################公司介绍
    intro=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[2]')[0]
    bug=intro.xpath('h5')[0]
    bug.clear()
    intro=intro.xpath('string(.)') 
    
    ################################规模
    scale=tree.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[1]/strong/text()')[0]
    scale=scale 
    
   
   
    #############################性质
    ctype=tree.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[2]/strong/text()')[0]
    ctype=ctype 
    
  
    ###########################
    writer.writerow((name,salary,addr,cname,scale,ctype))
    print('done')
    
gather=requests.get('http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&sm=0&p=1')
tree=etree.HTML(gather.text)
#//*[@id="newlist_list_content_table"]/table[2]/tbody/tr[1]/td[1]/div/a 无法直接定位由于
urls=tree.xpath('//*[@id="newlist_list_content_table"]/table/tr[1]/td[1]/div/a/@href') 
f=open(r'test.csv ','w')
head=csv.writer(f)
head.writerow(('name','wage','addr','companyname','scale','type'))


for url in urls:

    try:
        normal(url,f)#其中描述中的网址与其他叙述部分有粘连 有待改进
    except:
        print ('校园招聘:',url)
        time.sleep(1)
f.close()
