  # -*- coding: cp936 -*- 
#coding=utf-8
import requests
import time
import re
import pandas


#αװ�������
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}



def get_info(url):
    print('executing...',end='')
    
    res = requests.get(url,headers=headers)
    # ǰ�����ḽ��strong��ǩ ������Ϊ��ҳ��������������ǿ�������Ӵ֣�
    #�����Ƕ����� ֱ��ƥ�����ּ���  .*?���ڷ�̰��ƥ�����ⳤ����
    ranks = re.findall(r'<span class="pc_temp_num">.*?(\d{1,3}).*?</span>',res.text,re.S) 
    titles = re.findall(r'<li class=" " title="(.*?)" data-index=',res.text)    #data-index  ֵ���Ƕ�ֵ �۲�����ϸ
    times = re.findall(r'<span class="pc_temp_time">(.*?)</span>',res.text,re.S) 
    links=re.findall(r'<a href="(.*?)" data-active="playDwn"',res.text)
    downloads=get_download(links)
    
    for title,time,link,download in zip(titles,times,links,downloads):
        data = {
            '����':title.split('-')[0],
            '����':title.split('-')[1],
            'ʱ��':time.strip(),
            '���ŵ�ַ':link,
            '���ص�ַ':download
            }
        yield data

    print('done!') 
        
        

def get_download(urls): #���ݲ��ŵ�ַ������ص�ַ
    downloadURLs=[]
    for url in urls:
        playHTML=requests.get(url)#����ҳ��Դ��
        keyHash=re.search(r' var dataFromSmarty = \[\{"hash":"(.*?)"',\
                          playHTML.text)#��hash
        
        jsonURL=r'http://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'\
                             .format(keyHash.group(1))
        keyJson=requests.get(jsonURL)#��ȡ�ؼ�json�ļ�

        
        downloadURLs.append(keyJson.json()['data']['play_url'])
    return downloadURLs


        
if __name__ == '__main__':
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'\
            .format(str(i)) for i in range(1,4)]
    infoCollect=[]
    for url in urls:
        for each in get_info(url):
            
            infoCollect.append(each)
           


    df=pandas.DataFrame(infoCollect)
    df.to_excel('kugo.xlsx')
