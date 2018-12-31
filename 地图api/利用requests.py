# -*- coding: cp936 -*- 
#coding=utf-8
import requests
import json
import chardet
while(1):
    addr=input('输入地址：')
    #addr=addr.decode('gb18030').\
    #encode('utf-8')#gb18030在陌生编码，如ISO-8859-1下，尝试

    par={'address':addr,'key':'cb649a25c1f81c1451adbeca73623251'}#构造参数
    url='http://restapi.amap.com/v3/geocode/geo'
    res=requests.get(url,par)
    addr=res.text
    jsdt=json.loads(addr)
    try:
        print (jsdt['geocodes'][0]['formatted_address']\
               ,'坐标：',jsdt['geocodes'][0]\
               ['location'])
    except:
        print ('Not Found')



