# 面向对象
# 有意义的面向对象的代码
# 类 = 面向对象
# 类、对象
# 类最基本的作用：封装
# 实例化

# 类就像一个模板，实例化的对象就是根据模板创建出来的一个个具体的对象
class Student:
    name = 'zhangsan'
    age = 3

    def __init__(self, name, age):
        # 构造函数，实例化的时候会自动调用
        # 初始化对象的属性
        self.name = name
        self.age = age
        # print('student')

    # 行为 与 特性
    def do_homework(self):
        print('homework')
