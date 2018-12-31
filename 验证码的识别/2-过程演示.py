####以下每步都是过程讲解 并不连贯
import numpy as np
from sklearn.neural_network import MLPClassifier #类神经网络 多层分类器
from sklearn.preprocessing import StandardScaler #标准化在同一尺度
import matplotlib.pyplot as plt
import PIL
import os


####################读取图片#######
#为减少训练时间 需要将图像缩小
basewidth = 50

#读取图片并转为黑白色
pil_image = PIL.Image.open(r'D:\ChengXu\python\原生爬虫\验证码的识别\warehouse\A\1534556036.7179706_2.jpg').convert('1')
#pil_image

wpercent=(basewidth/float(pil_image.size[0])) #宽度缩放比例
hszie=int((float(pil_image.size[1])*float(wpercent))) #根据比例算出缩放高度
img = pil_image.resize((basewidth,hszie),PIL.Image.ANTIALIAS)
#img


#################将图标记并展示##########
digits=[]
labels=[]
basewidth = 50
fig = plt.figure(figsize=(20,20)) #显示缩略图
fig.subplots_adjust(left=0,right=1,top=1,hspace=0.5,wspace=0.5)# 排版调整
count = 0 #计数 subplot显示位置

path=r'D:\ChengXu\python\原生爬虫\验证码的识别\warehouse\{}'

# 65~90对应大写字母ascii
for i in range(65,91):
    
    for img in os.listdir(path.format(chr(i))):
        
        pil_image = PIL.Image.open((path+'\{}').format(chr(i),img))\
        .convert('1')
        
        wpercent=(basewidth/float(pil_image.size[0]))  
        hszie=int((float(pil_image.size[1])*float(wpercent))) 
        img = pil_image.resize((basewidth,hszie),PIL.Image.ANTIALIAS)
        
        ax = fig.add_subplot(20,12,count+1,xticks=[],yticks=[])
        ax.imshow(img,cmap=plt.cm.binary,interpolation='nearest')
        ax.text(0,7,chr(i),color='red',fontsize=20)
        count+=1
        
        digits.append([pixel for pixel in iter(img.getdata())])
        labels.append(chr(i))

###############数字化#####################
#digits 是一个嵌套列表 每一个列表元素又存放各图像素值
digit_ary = np.array(digits)
#digit_ary.shape  #得到二维数组 行数表图片数 列数表一张图像素的多少


###############标准化#############
scaler = StandardScaler()
scaler.fit(digit_ary)
X_scaled = scaler.transform(digit_ary)

#########训练##################
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30),activation='logistic',max_iter=30)
mlp.fit(X_scaled,labels)

#初步检验
predicted = mlp.predict(X_scaled)
target=np.array(labels)
target==predicted

#测试检验
data=[]
basewidth = 50
 

for img in os.listdir(r'D:\ChengXu\python\原生爬虫\验证码的识别\warehouse\测试'):      
    pil_image = PIL.Image.open((path+'\{}').format(r'测试',img))\
    .convert('1')
    print(pil_image.size)
    
    wpercent=(basewidth/float(pil_image.size[0]))  
    hszie=int((float(pil_image.size[1])*float(wpercent))) 
    img = pil_image.resize((basewidth,hszie),PIL.Image.ANTIALIAS)

    data.append([pixel for pixel in iter(img.getdata())])
scaler = StandardScaler()
scaler.fit(data)
data_scaled = scaler.transform(data)
print(data_scaled.shape)
print(mlp.predict(data_scaled))

