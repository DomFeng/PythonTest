# 概括字符集

import re
a = 'python1111java678php&\r\n__'

r1 = re.findall('\d', a)  # 匹配数字，等效r = re.findall('[0-9]', a) 
r2 = re.findall('\D', a)  # 匹配非数字，等效r = re.findall('[^0-9]', a) 
r3 = re.findall('\w', a)  # 匹配所有单词字符和数字，等效r = re.findall('[A-Za-z0-9_]', a)
r4 = re.findall('\W', a)  # 匹配所有非单词字符和数字，等效r = re.findall('[^A-Za-z0-9_]', a)
r5 = re.findall('\s', a)  # 匹配所有空白字符，等效r = re.findall('[\t\n\r\f\v]', a)
r6 = re.findall('\S', a)  # 匹配所有非空白字符，等效r = re.findall('[^\t\n\r\f\v]', a)
print(r4)