def squsum(*parames):
    sum = 0
    for i in parames:
        sum += i * i
        print ("i方=" + str(i*i))
    print(sum)

squsum(1,2,3,4,5,6)

# 设计一个函数支持任意个数的关键字参数