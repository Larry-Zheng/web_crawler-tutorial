由于网页在线运行 只允许导入内置包 
且input函数会递归报错 
所以写了一个urllib版本 可以在 在线编辑器上运行

在线编辑器网址：http://www.dooccn.com/python3/#contact

另外 在py3中
str ---(encode)---> bytes
bytes ---(decode)--->str

对于requests返回的response对象
其属性text 默认utf-8编码 是str类型
其属性content 未解码 是bytes类型