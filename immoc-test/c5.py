#函数参数
#1、必选参数
def add(x, y): #x,y为形参（形式参数）
    result = x + y
    return result
print(add(1, 2)) #1,2为实参（实际参数） 

#2、关键字参数
def add(x, y): 
    result = x + y
    return result

c = add(y=2, x=1)   #关键字参数,可以不按照形参顺序传递参数

