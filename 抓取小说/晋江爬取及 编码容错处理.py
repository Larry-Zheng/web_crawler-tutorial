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
    
    #�������޷�������ʾ can��t  decode xxx by ...
    #�����֮�� ���뷽ʽΪ Ī�����������������������ģ�
    #�ұ�����ŶȺܵ�ʱ
    #������ַ��ڸ��ű��� ������errors�������Դ���
    #�������Ĵ����� bs��etree���ܾ��޷������ݽ��н�����
    #����ֻ����reģ���������ץȡ
    
    res=res.content.decode('gb18030',errors='ignore')
    
    try:
        content=re.findall('(.*?)<br>',res)
        title=re.findall('<h2>(.*?)</h2>',res)
        title='���⣺'+title[0]
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
        print ('finished��')
        
        break
        
f.close()       

