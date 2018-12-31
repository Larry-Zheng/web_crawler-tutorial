import requests
from bs4 import BeautifulSoup

def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #半角空格直接转化                  
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

################################################
#获取源码
newsurl='http://news.sina.com.cn/china/'
res=requests.get(newsurl)
res.encoding='utf-8'
soup=BeautifulSoup(res.text,'lxml')

##############################################

header=soup.select('.news-item')#搜索属性为news-item的标签
for x in header:
    if len(x.select('h2'))>0:
        #在符合条件的标签里 再抓取时间标题
        time=x.select('.time')[0].text
        headline=x.select('a')[0].text.strip()
        link=x.select('a')[0]['href']

        #这里的对齐问题属于全角半角问题
        #不对齐产生原因 详见 http://lib.csdn.net/article/python/66507?knId=160
        #不对齐解决办法 详见 https://www.cnblogs.com/kaituorensheng/p/3554571.html

        #注释掉的这种方法看似可以对齐 但实际上不行 不妨尝试一下 
        #print ('%(time)-15s %(headline)-50s %(link)-100s'\
        #      %{'time':time,'headline':headline,'link':link},'\n')
        
        print(time.ljust(15),strB2Q(headline.ljust(30)),link.ljust(50))
        #对于上面这条语句 这里还有一个小问题
        #输出的第二项可不可以写成 strB2Q(headline).ljust(30) 呢？
        #即 先统一全角半角 再填充左对齐 是否可行呢？
        
        #提示:①ljust函数第二个参数 传入字符串 如'+' 可以规定填充样式
             #②根据上一条提示 观察 填充的字符串是半角还是全角
        
        #参考上面strB2Q函数中的全角空格（chr(12288)）
        #再想一想 若我非要先统一全角半角 再填充左对齐 应该怎么办？
        
