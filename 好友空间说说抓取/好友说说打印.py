# -*- coding: UTF-8 -*-
#还需进一步修改 获取mainpage里的uin
import sys  
import re
import requests
import time
import pprint
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool
from functools import partial

#####################################################破译gtk码
def LongToInt(value):  # 由于int+int超出范围后自动转为long型，通过这个转回来  
    if isinstance(value, int):  
        return int(value)  
    else:  
        return int(value & sys.maxint)  
def LeftShiftInt(number, step):  # 由于左移可能自动转为long型，通过这个转回来  
    if isinstance((number << step), int):
        return int((number << step) - 0x200000000)
    else:  
        return int(number << step)  
def getNewGTK(p_skey, skey, rv2):  
    b = p_skey or skey or rv2  
    a = 5381  
    for i in range(0, len(b)):  
        a = a + LeftShiftInt(a, 5) + ord(b[i])  
        a = LongToInt(a)  
    return a & 0x7fffffff
##################################################
def exe(qqnum,file):
    url='https://user.qzone.qq.com/{}/311'.format(qqnum)
    # url='https://user.qzone.qq.com'
    mainpage='https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={}&ftype=0&sort=0&pos={}&num=20&replynum=100&g_tk={}'
##################以上js三参数 访问的qq页码*20和key
    # 创建chrome参数对象
    opt = webdriver.ChromeOptions()

    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.set_headless()
    driver=webdriver.Chrome(options=opt)
    driver.maximize_window()
    driver.get(url)

    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()

    a=driver.find_element_by_id('u') 
    a.clear()
    a.send_keys('519334736')
    b=driver.find_element_by_id('p') 
    b.clear()
    b.send_keys('')#mi6 agent7 pineapple
    driver.find_element_by_id('login_button').click()
    time.sleep(3)
    driver.implicitly_wait(5)
##############################################
    keys=driver.get_cookies()

    check=0#加快检查
    #keys里三参数的位置随时在变，只能搜出来
 
    r=' '#用于登自己空间
    for key in keys:
        if 'name' in key.keys():
            if key['name']=='p_skey':
                p=key['value']
                check=check+1
            if key['name']=='skey':
                s=key['value']
                check=check+1
            if key['name']=='rv2':
                r=key['value']
                check=check+1
        if check==3:
            break 
 
    silver=getNewGTK(p, s, r)  
 ###################################################
    pos=0
    while 1:
        dividpage=mainpage.format(qqnum,pos,silver)
        driver.get(dividpage)
        driver.implicitly_wait(10)
        #print driver.current_url  打印url和page都不用括号
        a=driver.page_source
        prefix='<html xmlns="http://www.w3.org/1999/xhtml">\
        <head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">_Callback('
        suffix=');</pre></body></html>'
        a=a.lstrip(prefix).rstrip(suffix)
        print(a)
        #pprint.pprint(jd) 结构化打印方法
 
        jd=json.loads(a)
        msglist=jd['msglist']
        try:
            for msg in msglist:
                saysay=msg['content']
                # print (saysay)
                f.write(saysay)
            pos=pos+20
        except Exception as e:
            print(type(e))
            print(e)
            break
    driver.close()
##########################################
if __name__=="__main__":   
    qq=['842168590']
    #清除数据
    with open('qqsaysay.txt','w') as f:
        f.write('')
    f=open('qqsaysay.txt','a+',encoding='utf-8')
    t1=time.time()
    exe(qq[0],f)

    t2=time.time()
    print (t2-t1)
    '''t3=time.time()
    pool=Pool(processes=4)
    constexe=partial(exe,file=f)
    pool.map(constexe,qq)
    t4=time.time()
    print t4-t3''' 
    f.close()
