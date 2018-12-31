  # -*- coding: cp936 -*- 
#coding=utf-8
import requests
import time
import re
import pandas


#伪装成浏览器
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}



def get_info(url):
    print('executing...',end='')
    
    res = requests.get(url,headers=headers)
    # 前三名会附带strong标签 这是因为网页对这三个进行了强调（变红加粗）
    #且我们对排名 直接匹配数字即可  .*?用于非贪婪匹配任意长内容
    ranks = re.findall(r'<span class="pc_temp_num">.*?(\d{1,3}).*?</span>',res.text,re.S) 
    titles = re.findall(r'<li class=" " title="(.*?)" data-index=',res.text)    #data-index  值不是定值 观察需仔细
    times = re.findall(r'<span class="pc_temp_time">(.*?)</span>',res.text,re.S) 
    links=re.findall(r'<a href="(.*?)" data-active="playDwn"',res.text)
    downloads=get_download(links)
    
    for title,time,link,download in zip(titles,times,links,downloads):
        data = {
            '歌手':title.split('-')[0],
            '歌曲':title.split('-')[1],
            '时长':time.strip(),
            '播放地址':link,
            '下载地址':download
            }
        yield data

    print('done!') 
        
        

def get_download(urls): #根据播放地址解出下载地址
    downloadURLs=[]
    for url in urls:
        playHTML=requests.get(url)#播放页面源码
        keyHash=re.search(r' var dataFromSmarty = \[\{"hash":"(.*?)"',\
                          playHTML.text)#找hash
        
        jsonURL=r'http://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'\
                             .format(keyHash.group(1))
        keyJson=requests.get(jsonURL)#获取关键json文件

        
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
