# json 反序列化
import json
# 对于json中的字符串，需要用双引号引起来，最外层字符串在python中用单引号
json_str = '{"name":"qiyue", "age":18}'
student = json.loads(json_str)
print(type(student))  # python反序列化后为字典类型
print(student)

# 访问字典内容
print(student['name'])
print(student['age'])


# 数组反序列化
json_str_array = '[{"name":"qiyue", "age":18, "flag":false},{"name":"qiyue", "age":18}]'
student1 = json.loads(json_str_array)
print(type(student1))  # 数组反序列化后为列表类型
print(student1)

# 访问列表内容
print(student1[0]['name'])