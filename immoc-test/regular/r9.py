import re
lanuage = 'PythonC#\nJavaPHP'

# re.I表示忽略大小写,re.S表示匹配换行符,|表示同时支持多种模式
r = re.findall('c#.{1}', lanuage, re.I | re.S) 
print(r)