import requests
import chardet
import re
res=requests.get('https://jobs.51job.com/chengdu-pdq/93758731.html?s=01&t=0')

#查编码
method=chardet.detect(res.content)['encoding']#查内容编码
main=res.content.decode(method).encode('utf-8').decode('utf-8')

#当br不是成对存在
#无法解析 而附带在内容里时
#将br去掉
main=re.sub('<br>','',main)

contents=re.findall('<p>(.*?)</p>',main,re.S)#搜具体职位的p标签内容
 
for content in contents:
    print (content)
