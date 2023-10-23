c = 1

def  func1():
    c = 2
    print(c)
    def func2():
        c = 3
        print(c)
    func2()
func1()