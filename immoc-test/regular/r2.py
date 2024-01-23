import re

a = 'COC++7Java8C#9Python6Javascript'

# 将字符串中的数字提取出来
r = re.findall('\d', a)     # \d表示数字
r1 = re.findall('\D', a)     # \D表示非数字
print(r)
print(r1)

# 'Python' 普通字符
# '\d' 元字符