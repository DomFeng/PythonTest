class Student():
    name = 'qiyue'
    age = 0
    
    # 类变量  实例变量
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def do_homework(self):
        print('homework')
        
student1 = Student('石敢当', 18)
student2 = Student('喜小乐', 19)
print(student1.name)
print(student2.name)
print(Student.name)