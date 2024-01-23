import re
s = 'life is short, i use python, i love python'

# 提取life和python的中间的字符
r = re.search('life(.*)python(.*)python', s)
# group(0)表示匹配到的所有内容，默认
print(r.group(0))
# 访问group(1)，获取第一个括号中匹配到的内容
print(r.group(1))
# ...
print(r.group(2))

# group(0,1,2)表示匹配到的所有内容
print(r.group(0,1,2))
# groups()方法返回所有括号中的内容
print(r.groups())