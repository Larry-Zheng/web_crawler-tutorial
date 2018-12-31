import requests
from bs4 import BeautifulSoup
import os

##########################
#获取图片下载地址
res=requests.get('https://tieba.baidu.com/p/5534091070')
soup=BeautifulSoup(res.text,'html.parser')
pics=soup.select('.BDE_Image')
local=[]
for pic in pics:
    local.append(pic['src'])
    
################################    
#创建或生成 文件夹
def makeFolder(path):
    judge=os.path.exists(path) #判断路径是否存在
    if not judge:
        try:
            os.makedirs(path) #不存在 生成文件夹
        except OSError:
            print('请检查文件的命名！')
            exit(1)


for i,img in enumerate(local[:20]): #只取前20张做测试
    picReq=requests.get(img) #获取图片的response对象
    
    path=r'./二进制写入测试/'
    makeFolder(path)  #路径初始化
    
    #以二进制写图片
    with open(path+str(i)+'.jpg','wb') as f:
        print('executing{}...'.format(i),end=' ')
        print(img)
        print(picReq.content)
        f.write(picReq.content)
        print('done！')
