'''
    a test py
'''

ACCOUNT = 'qiyue'
PASSWORD = '123456'

# python 建议用_ 分割变量名

# 提示用户输入账号
print('请输入账号')
user_account = input()
# 提示用户输入密码
print('请输入密码')
user_password = input()
# 检查用户输入的账号和密码是否与预设值匹配
if user_account == ACCOUNT and user_password == PASSWORD:
    print('登录成功')
else:
    print('登录失败')


