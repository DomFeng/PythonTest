class Human():
    
    sum = 0
    
    def __init__(self, name ,age):
        self.name = name
        self.age = age

    def get_name(self):
        print('获取姓名：' + self.name)
        
    def do_homework(self):
        print('do homework')