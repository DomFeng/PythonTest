import re
lanuage = 'PythonC#JavaC#PHPC#'


def convert(value):
    # value是对象,可以调用group()方法显示匹配到的字符串
    matched = value.group()
    return '!!' + matched + '!!'

# C#替换成GO
# re.sub()表示替换,0表示替换所有匹配到的字符串
r = re.sub('C#','GO',lanuage, 0)
# sub()方法第二个参数可以是函数,如果匹配到C#,就调用convert函数
r = re.sub('C#',convert,lanuage, 0)
print(r)

# 使用replace()方法也可以实现替换
lanuage = lanuage.replace('C#','GO')
print(lanuage)