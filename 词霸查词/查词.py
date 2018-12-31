
import requests
from lxml import etree

while 1:
    word=input('请输入一个单词：')
    para={
        'a':'getWordMean',
        'c':'search',
        'list':'1,2,3,4,5,8,9,10,12,13,14,15,18,21,22,24,3003,3004,3005',
        'word':word,
        
    }
    
    
    res=requests.get('http://www.iciba.com/index.php',params=para)
    dictionary=res.json()
    
    
    try:
        #英标
        egAccent=dictionary['baesInfo']['symbols'][0]['ph_en']
        amAccent=dictionary['baesInfo']['symbols'][0]['ph_am']
        print('英音%-9s'%egAccent,'美音：',amAccent)
        #意思
        for item in dictionary['baesInfo']['symbols'][0]['parts']:
            print('形式：%-5s'%item['part'],' ','意思：',('、').join(item['means']))
    except KeyError:
        print('Sorry~ 没找到这个单词')
    finally:
        print('\n\n')
