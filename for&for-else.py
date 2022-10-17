# 主要是用来遍历\循环  序列或者集合\字典
# a = [['a', 'b', 'c', 'd'], (1, 2, 3)]
# for x in a:
#     for y in x:
#         print(y, end='')

b = [1, 2, 3]
for y in b:
    if y == 2:
        continue
    print(y)

