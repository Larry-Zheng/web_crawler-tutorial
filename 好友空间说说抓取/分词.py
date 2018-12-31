import jieba.analyse
path=r'E:\keyword extraction\content.txt'
fp=open(path,'rb')
content=fp.read()
 
 

try:   
    jieba.analyse.set_stop_words(r'E:\keyword extraction\new.txt')
    tags=jieba.analyse.extract_tags(content,topK=500,withWeight=True)
    for item in tags:
        if item[0][0].isdigit() or item[0][0]=='e':
            continue
        print item[0]
        #print item[0]+'\t'+str(int(item[1]*1000))
finally:
    fp.close()
