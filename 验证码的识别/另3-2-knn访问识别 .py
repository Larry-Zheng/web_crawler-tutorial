from sklearn.externals import joblib
import requests
from PIL import Image
import numpy as np 
from matplotlib import pyplot as plt
# from sklearn.preprocessing import StandardScaler
import cv2
import os

clf = joblib.load('captcha.pkl') #导入模型

#访问原始验证码 存入本地
rs = requests.session()
with open(r'kaptcha.jpg','wb') as f:
    res = rs.get('http://jiaowu.swjtu.edu.cn/servlet/GetRandomNumberToJPEG')
    f.write(res.content)
    


#读取图片的数字信息
pil_image=Image.open(r'kaptcha.jpg').convert('RGB')
open_cv_image=np.array(pil_image)
print(plt.imshow(open_cv_image)) #绘图


##################字母切分#################
basewidth = 50
def saveKaptcha(image):

    #读取图片的数字信息
    pil_image=Image.open(image).convert('RGB')
    open_cv_image=np.array(pil_image)
    #print(plt.imshow(open_cv_image)) #绘图


    imgray= cv2.cvtColor(open_cv_image,cv2.COLOR_BGR2GRAY)#转灰阶
    
    
    imgray[0:2]=255 #非常重要 图像顶部横线 和左边竖线 去掉 便于识别
    imgray[:,0:2]=255 #取一列的方法
    ret,thresh= cv2.threshold(imgray,100,255,0)
    image,countours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,\
                cv2.CHAIN_APPROX_SIMPLE)
    cnts= sorted([(c,cv2.boundingRect(c)[0]) for c in countours], key = lambda x: x[1])
    ary=[]
    for (c,_)  in cnts:
        (x,y,w,h)=cv2.boundingRect(c)
        #字符高 在15左右 且排除连笔 以此判别 
        if 10<h<20 : #不能对宽度进行修饰限定 比如 i 和 w 
            ary.append((x,y,w,h))
            #存图

    if len(ary) !=4:
        print('截取有误')
        exit(1)
         
    for id,(x,y,w,h) in enumerate(ary):
        fig=plt.figure()
        roi=thresh[y:y+h,x:x+w]
        #thre=roi.copy()
        plt.imshow(roi)
        plt.savefig('.\workspace\{}.jpg'.format(id+1),dpi=100)
        plt.close()
###############################################
        
saveKaptcha('kaptcha.jpg')  

############标准化与识别####################
def predict():
    data=[]
    for img in os.listdir(r'.\workspace'):
        pil_image = Image.open(r'.\workspace\%s'%img).convert('1')
       
        r'''        wpercent=(basewidth/float(pil_image.size[0]))  
        hszie=int((float(pil_image.size[1])*float(wpercent))) '''

        #这里标准直接抓取下来的大小 应该是640*480 而有时截取会有偏差 导致最后矩阵乘法无法进行 
        #索性 我们直接将缩放后的尺寸算出 50*37
        img = pil_image.resize((50,37),Image.ANTIALIAS)

        data.append([pixel for pixel in iter(img.getdata())])
        

    
    print(clf.predict(np.array(data)))
    
predict()
        
