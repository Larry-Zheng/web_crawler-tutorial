############本文件只作下载测试用##############################
import requests
import re
import time
a=requests.session()
b=a.get('http://www.kugou.com/song/mfv56b9.html')
#print(b.text)
k=re.search(r' var dataFromSmarty = \[\{"hash":"(.*?)"',b.text)
print(k.group(1))

target='http://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'.format(k.group(1))
mp3=requests.get(target)
download=mp3.json()['data']['play_url']
print(download)

download=requests.get(download)
with open('test.mp3','wb') as f:
    f.write(download.content)
    
