import matplotlib.pyplot as plt
import os,PIL
import numpy as np
# from  sklearn.preprocessing import StandardScaler
# from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.model_selection import train_test_split


digits = [] #嵌套列表 存各图像像素点数据
labels = [] #一维列表 存各图像的数据标签

basewidth = 50 #规定 图像缩放的宽度


#shift+tab jupyter提示
#分两层循环 第一层遍历大写字母 A-Z
#第二层 遍历各文件夹下的图像
#这样一类图像将贴上相同标签
for i in range(65,91): #65-91 对应 A~Z ascii
    for img in os.listdir(r'.\warehouse\{}'.\
                          format(chr(i))):
        pil_img=PIL.Image.open\
        (r'.\warehouse\{}\{}'.format(chr(i),img))\
        .convert('1')  #读图并转黑白

        #将图像缩放
        #缩放图像的意义在于加快训练
        #（若不缩放 风扇会狂转 电脑迅速升温 也根本带不动） 
        
        #这里有时会出一个小bug 在于
        #我们抓取下来的的字母图片 有时不是标准的640*480  
        #若不解决 这会带来维度的不统一 影响后面的训练
        #若出现上述情况 我们索性直接算出缩放后的图像尺寸 50*37
        wprecent = (basewidth/float(pil_img.size[0]))
        hsize = int(float(pil_img.size[1])*float(wprecent))
        # print(bandwidth,hsize) #查看维度是否统一
        img = pil_img.resize((basewidth,hsize),PIL.Image.ANTIALIAS)
        
        
        #注意img.getdata()只是一个可迭代对象 用iter 或 list 让其可遍历
        digits.append([pixel for pixel in iter(img.getdata())]) 
        labels.append(chr(i))





X_raw = np.array(digits) #转np
y_raw = np.array(labels)
X_train,X_test,y_train,y_test = train_test_split(X_raw,y_raw,\
        test_size=0.2)
#print(digit_ary.shape)
#查看 shape值为 （240，1850）
#表示 有240张图将送入训练 每张图有1850个pixel
#1850也将是后面训练模型的标准
#最后我们待读图像的像素个数标准 必须是1850





#训练
# knnClf = KNeighborsClassifier(n_neighbors=9)
# knnClf.fit(X_train,y_train)
# print(knnClf.score(X_test,y_test))


#确定最佳超参数
best_k = -1
best_score = 0.0


for k in range(1,len(X_train)+1):
    knnClf = KNeighborsClassifier(n_neighbors=k)
    knnClf.fit(X_train, y_train)
    current_score = knnClf.score(X_test,y_test)
    if current_score > best_score:
        best_score = current_score
        best_k = k

print(best_k,best_score)


#模型存档
knnClf = KNeighborsClassifier(n_neighbors=best_k)
knnClf.fit(X_train, y_train)
joblib.dump(knnClf,'KNNcaptcha.pkl')
