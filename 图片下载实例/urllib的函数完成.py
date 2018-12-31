from urllib import request
import re
import os


##########################
# 访问并获取'https://tieba.baidu.com/p/5534091070'源码
def getHTML(url):  # 获取源码
    resp = request.urlopen(url)

    # 注意 直接读取的是bytes 解码后变成str
    # 不再是unicode与str之间折腾
    html = resp.read().decode('utf-8')
    return html


##################################
def getPicURLs():
    picHTML = getHTML('https://tieba.baidu.com/p/5534091070?pn=1')

    # 这里re与BS搜出来的图片有一个微小差别 在于
    # BS 搜出的class 属性 必须有BDE
    # 而re没加限制(其实也可以加)
    # 所以 re搜出的第一张是空白图片 比BS多搜出来一张
    rule = r'src="(https://.*?\.jpg)"'  # 注意https 这个bug

    picURLs = re.findall(rule, picHTML)
    print('There can be {} pictures to load!'.format(len(picURLs)))
    return picURLs


################################
# 创建或生成 文件夹
def makeFolder(path):
    judge = os.path.exists(path)  # 判断路径是否存在
    if not judge:
        try:
            os.makedirs(path)  # 不存在 生成文件夹
        except OSError:
            print('请检查文件的命名！')
            exit(1)


path = r'./urlretrieve函数下载/'
makeFolder(path)
for i, eachURL in enumerate(getPicURLs()[:20]):
    print(r'executing no.{}...'.format(i), end=' ')
    request.urlretrieve(eachURL, path + str(i) + '.jpg')
    print('done！')
