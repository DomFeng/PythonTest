# 数量词
# * 表示对前一个字符匹配0次或者无限多次
# + 表示对前一个字符匹配1次或者无限多次
# ? 表示对前一个字符匹配0次或者1次
import re
a = 'pytho0python1pythonn2'

r = re.findall('python*', a) # *表示对前一个字符匹配0次或者无限多次
print(r)