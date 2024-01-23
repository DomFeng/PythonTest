from t5 import Human

class Student(Human):

    def __init__(self, school, name, age):
        self.school = school
        # 在字类中调用父类的构造函数,self必须是第一个参数
        # Human.__init__(self, name, age)
        
        # 使用super函数调用父类的构造函数
        super(Student, self).__init__(name, age)
    
    def do_homework(self):
        # 调用父类的方法
        super(Student, self).do_homework()
        print('english homework')
        
student1 = Student('清华大学', '石敢当', 18)
# print(student1.name)
# print(student1.age)

# 调用父类的方法
# student1.get_name()
# 调用子类的方法
# student1.dom_home_work()

# 如果子类方法与父类方法同名，子类方法会覆盖父类方法
student1.do_homework()