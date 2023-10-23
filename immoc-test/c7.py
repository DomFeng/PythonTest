# 定义一个可变参数的函数
def demo(*param):
    print(param)
    print(type(param))


demo(1, 2, 3, 4, 5)


# 等同于：定义普通参数的函数，传递元组
def demo1(param):
    print(param)
    print(type(param))


demo1((1, 2, 3, 4, 5, 6))

a = (1, 2, 3, 4, 5, 6, 7)
demo(a)  #等同于demo((1,2,3,4,5,6,7),)  会变成二维元组
demo(*a)  #等同于demo(a[0],a[1],a[2],a[3],a[4],a[5],a[6])

# 必须参数、关键参数、可变参数
def demo2(param1, param2=2, *param):
    print(param1)
    print(param2)
    print(param)

demo2('a',1,2,3)
    