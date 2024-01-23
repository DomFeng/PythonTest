# import sm3相关模块
import sm3

a = 'jszd00000'
# sm3加密变量a的值
print(sm3.sm3_hash(a))
# sm3加密变量a的值的前16位
print(sm3.sm3_hash(a)[:16])
# sm3加密变量a的值的前16位的大写
print(sm3.sm3_hash(a)[:16].upper())
# sm3加密变量a的值的前16位的大写的前8位
print(sm3.sm3_hash(a)[:16].upper()[:8])
# sm3加密变量a的值的前16位的大写的前8位的ASCII码
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][0]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][1]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][2]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][3]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][4]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][5]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][6]))
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][7]))
# sm3加密变量a的值的前16位的大写的前8位的ASCII码的和
print(ord(sm3.sm3_hash(a)[:16].upper()[:8][0]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][1]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][2]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][3]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][4]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][5]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][6]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][7]))
# sm3加密变量a的值的前16位的大写的前8位的ASCII码的和的16进制
print(hex(ord(sm3.sm3_hash(a)[:16].upper()[:8][0]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][1]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][2]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][3]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][4]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][5]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][6]) + ord(sm3.sm3_hash(a)[:16].upper()[:8][7])))
