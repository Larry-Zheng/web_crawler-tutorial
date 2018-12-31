import requests
import chardet
from bs4 import BeautifulSoup
res=requests.get('https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1')
 
print (chardet.detect(res.content))
#res.text默认强行解码utf-8，在乱码情况下用content以bit读出。若content还是有乱码
#我们需要在此查看content的编码规则，decode对应编码再做utf-8处理
