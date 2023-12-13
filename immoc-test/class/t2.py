def calculator():
    # 获取用户输入的表达式，去掉空格和换行符
    expression = input("请输入要计算的表达式: ").strip()
    # 判断表达式是否为空
    if not expression:
        print("请输入有效的表达式")
        return
    # 使用 try-except 语句来处理可能出现的异常
    try:
        # 使用 eval 函数来计算表达式的值，并保留两位小数
        result = round(eval(expression), 2)
        # 打印计算结果
        print(f"计算结果为: {result}")
    except Exception as e:
        # 如果出现异常，打印异常信息
        print(f"计算出错: {e}")

# 调用函数
calculator()