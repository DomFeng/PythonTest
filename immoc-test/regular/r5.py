# 数量词
# * 匹配0次或者无限多次
import re
a = 'python 1111java678php'
# 匹配所有单词
r = re.findall('[a-z]{3,6}', a) # {3,6}表示匹配3到6个字符

# 贪婪与非贪婪
# 贪婪：尽可能多的匹配，非贪婪：尽可能少的匹配
# python默认贪婪
r = re.findall('[a-z]{3,6}?', a) # ？表示非贪婪，尽可能少的匹配

print(r)