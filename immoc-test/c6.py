def print_student_files(name,gender='男',age='18',college='北京大学'):  # 默认参数
    print("我叫" + name)
    print("我今年" + str(age) + "岁")
    print("我是" + gender + "生")
    print("我在" + college + "上学")

print_student_files("鸡小萌")
# 实参覆盖默认参数
print_student_files("消消乐",age=20,college="清华大学")

# 形参-默认参数-形参，这种结构是不允许的
def print_student_filess(name,gender='男',age='18',college='北京大学',teacher):
        
# 没有明确指定参数值的情况下，实参会根据形参的顺序进行赋值
print_student_files("果果",23) # 23会赋值给gender

# 不能将默认参数和关键字参数混用
print_student_files("果果",gender="女",age=23,college="清华大学")