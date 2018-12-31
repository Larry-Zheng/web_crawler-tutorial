import requests
from lxml import etree
import time
def normal(url):
    res=requests.get(url)
    tree=etree.HTML(res.text)
    name=tree.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()')
    ########################职位名
    print ('职位：',name[0])
    ######################基本工资和福利
    bonus=tree.xpath('/html/body/div[5]/div[1]/div[1]/div[1]/span/text()') 
    basic=tree.xpath('/html/body/div[6]/div[1]/ul/li[1]/strong/text()')
    salary=[]
    salary.extend(basic)
    salary.extend(bonus)
    salary=(u'、').join(salary)
    print ('待遇：',salary)
    ##############################地址
    addr=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/h2/text()')
    addr=addr[0].strip()
    print ('工作地址：',addr)
    #########################具体描述
    dscr=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/p')
    print ('描述：')
    for d in dscr:
        print ('\t'+d.xpath('string(.)'))
    ##########################公司介绍
    intro=tree.xpath('/html/body/div[6]/div[1]/div[1]/div/div[2]')[0]
    intro=intro.xpath('string(.)')
    intro=intro.replace('  ','')
    intro=intro.replace(u'该公司其他职位','')
    print ('公司及简介：\n',intro.strip())
    ################################规模
    scale=tree.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[1]')[0]
    scale=scale.xpath('string(.)')
    print ('\n',scale)
    #############################性质
    ctype=tree.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[2]')[0]
    ctype=ctype.xpath('string(.)')
    print (ctype,'\n\n')
    ###########################
gather=requests.get('http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&sm=0&p=1')
tree=etree.HTML(gather.text)
#//*[@id="newlist_list_content_table"]/table[2]/tbody/tr[1]/td[1]/div/a 无法直接定位由于
urls=tree.xpath('//*[@id="newlist_list_content_table"]/table/tr[1]/td[1]/div/a/@href') 
for url in urls:
    try:
        normal(url)#其中描述中的网址与其他叙述部分有粘连 有待改进
    except:
        print ('校园招聘:',url)
    print('#################################################')
    time.sleep(1)
