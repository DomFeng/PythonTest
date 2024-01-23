class Student():
    name = 'qiyue'
    age = 0
    sum = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__score = 0
        # self.__class__.sum += 1     # 操作类变量
        # print('当前版本学生总数为：' + str(self.__class__.sum))
        # print(Student.sum1)   # 在实例方法中访问类变量方法1
        # print(self.__class__.sum1)  # 在实例方法中访问类变量方法2
        # print(self.name)    # self.name是实例变量，作用域是整个类
        # print(name1)    # name1是形参，只在init函数中有效
        
    def marking(self,score):
        if score < 0:
            return '不能打负分'
        else:
            self.__score = score
            return self.name + '同学本次考试分数为：' + str(self.__score)
            # print(self.name + '同学本次考试分数为：' + str(self.score))
    
    
    def do_homework(self):
        self.do_english_homework()
        print('homework')
        
    def do_english_homework(self):
        print('english homework')
        
    # 定义类方法，需要定义@classmethod装饰器，第一个参数必须是cls
    @classmethod
    def plus_sum(cls):
        cls.sum += 1
        print(cls.sum)
    
    # 定义静态方法，需要定义@staticmethod装饰器
    @staticmethod
    def add(x,y):
        print(Student.sum)  # 静态方法访问类变量
        print('This is a static method')
    # 不建议使用静态方法，因为与实例和类关联性不大 
     
        


# Student.plus_sum()
# student2 = Student('喜小乐', 19)
# Student.plus_sum()
# student3 = Student('王大锤', 20)
# Student.plus_sum()

# student1.plus_sum()     # 实例对象也可以调用类方法，但是不建议这么做

# student1.add(1,2)
# Student.add(1,2)
student1 = Student('石敢当', 18)
student2 = Student('喜小乐', 19)
print(student1.marking(3))

# score变量目前是公开的 public  私有的 private
# 动态添加私有变量
student1.__score = -1

#可以通过打印__dict__查看实例变量
print(student1.__dict__)

#访问私有变量，python解释器会把__score变量改成_Student__score
print(student1._Student__score)
# print(student1.__score)
# print(student2.__score)