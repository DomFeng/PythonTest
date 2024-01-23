import re
s = '83C72D1D8E67'

# match从首字母开始匹配，如果没有找到，返回None
r = re.match('\d' , s)
print(r)

# search从任意位置匹配，尝试搜索整个字符串，直到找到一个匹配
r1 = re.search('\d' , s)
print(r1)

# 使用group()方法获取匹配的结果
print(r1.group())
# span()方法返回匹配的位置
print(r1.span())  
# findall()方法返回所有匹配的结果
r2 = re.findall('\d' , s)
print(r2)