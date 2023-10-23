a = 1
b = 2
c = 3

a, b, c = 1, 2, 3

d = 4, 5, 6
print(type(d))

a, b, c = d
print(a, b, c)

# 给两个变量赋值三个值，报too many values to unpack
a, b = [1, 2, 3]

#链式赋值
a = b = c = 1
print(a, b, c)
