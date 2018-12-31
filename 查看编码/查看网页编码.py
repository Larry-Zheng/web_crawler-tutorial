from urllib import request
fopen1 = request.urlopen('http://jobs.zhaopin.com').info()
print (fopen1)
