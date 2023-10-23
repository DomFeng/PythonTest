def city_temp(**parames):
    #遍历字典
    for key,value in parames.items():
        print(key,":",value)

a = {'bj':'20c','sh':'30c','gz':'25c'}
city_temp(**a)  # **a表示将字典a拆分为关键字参数传递给函数