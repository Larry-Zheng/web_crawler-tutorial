import cv2
import requests
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import time
import os 

def crawlKaptcha():

    #时间戳
    timemark=str(time.time())

    #抓图
    with open(r'kaptcha.jpg','wb') as f:
        res = requests.get('http://jiaowu.swjtu.edu.cn/servlet/GetRandomNumberToJPEG')
        f.write(res.content)



    #读取图片的数字信息
    pil_image=Image.open(r'kaptcha.jpg').convert('RGB')
    open_cv_image=np.array(pil_image)
    #print(plt.imshow(open_cv_image)) #绘图


    #读完就删
    os.remove(r'kaptcha.jpg')


    imgray= cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2GRAY)#转灰阶

    imgray[0:2]=255 #非常重要 图像顶部横线 和左边竖线 去掉 便于识别
    imgray[:,0:2]=255 #取一列的方法



    ret,thresh= cv2.threshold(imgray,100,255,0) #设立阈值 滤波 返回图像thresh
    #print(plt.imshow(thresh))

    #参数 矩形轮廓 水平垂直压缩留下中点坐标
    #返回的counters 是物体的轮廓 
    image,countours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_SIMPLE)
    

    print(plt.imshow(thresh))
        
    #排序
    #将刚刚检测出的各轮廓 用最小的矩形框起来
    cnts= sorted([(c,cv2.boundingRect(c)[0]) for c in countours], key = lambda x: x[1])

    ary=[]
    for (c,_)  in cnts:
        (x,y,w,h)=cv2.boundingRect(c)
        #字符高 在15左右 且排除连笔 以此判别 
        if 10<h<20 : #不能对宽度进行修饰限定 比如 i 和 w 
            ary.append((x,y,w,h))
        
        
    #存图
    for id,(x,y,w,h) in enumerate(ary):
        fig=plt.figure()
        roi=thresh[y:y+h,x:x+w]
        #thre=roi.copy()
        plt.imshow(roi)
        plt.savefig('.\warehouse\%s_{}.jpg'.format(id+1)%(timemark),dpi=100)
        plt.close()
    time.sleep(1)

for i in range(50):
    crawlKaptcha()
    
    
