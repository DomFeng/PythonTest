import re
a = 'PythonPythonPythonPythonPython'
# 判断字符串中是否包含3个python
r = re.findall('(Python){3}', a)
print(r)
