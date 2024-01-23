import re
s = 'A8C3721D86'

# 找出字符串中所有的大于等于6的数字替换为9，小于6的数字替换为0
def convert(value):
    matched = value.group()
    if int(matched) >= 6:
        return '9'
    else:
        return '0'

r = re.sub('\d',convert,s)
print(r)
