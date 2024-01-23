# 边界匹配符
import re
qq = '100000001'
# 匹配4-8位的qq号码
r = re.findall('\d{4,8}', qq)
# ^ 匹配字符串开头  $ 匹配字符串结尾，意在匹配完整字符串
r = re.findall('^\d{4,8}$', qq)
print(r)