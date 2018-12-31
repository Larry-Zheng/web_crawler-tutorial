#!/usr/bin/python
# -*- coding: utf-8 -*-import
import urllib
from urllib import request
import json

address='犀浦'
#addr=addr.decode('gb18030').encode('utf-8')#gb18030在陌生编码，如ISO-8859-1下，尝试
par={'address':address,'key':'cb649a25c1f81c1451adbeca73623251'}

url='http://restapi.amap.com/v3/geocode/geo'

#将参数列表解析 且还必须转为bytes类型
data= urllib.parse.urlencode(par).encode('utf-8')
addr=request.urlopen(url,data).read().decode('utf-8')
jsdt=json.loads(addr)
try:
    print (jsdt['geocodes'][0]['formatted_address']\
           ,'坐标：',jsdt['geocodes'][0]\
           ['location'])
except:
    print ('Not Found')
