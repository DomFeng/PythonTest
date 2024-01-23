import re
s = 'abc, acc, adc, aec, afc, ahc'

# 找出中间字符为c或f的字符串
r1 = re.findall('a[cf]c', s)     # 中括号[]表示或
r2 = re.findall('a[^cf]c', s)     # 中括号[]中^表示非
r3 = re.findall('a[c-f]c', s)     # 中括号[]中-表示c到f所有的字符
print(r1)
print(r2)
print(r3)