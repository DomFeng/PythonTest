'''
    a test py
'''

ACCOUNT = 'qiyue'
PASSWORD = '123456'

# python 建议用_ 分割变量名
print('please input account')
user_account = input()

print('please input password')
user_password = input()

if user_account == ACCOUNT and user_password == PASSWORD :
    print('login success')
else :
    print('login fail')
