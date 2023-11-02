import pandas as pd

# CSV文件路径
csv_file = "D:\\202310312103.csv"  # 请替换成你的CSV文件路径

# 读取CSV文件
data = pd.read_csv(csv_file)
# 不使用科学计数法
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# 打印data的前5行
# print(data.head(5))

# 打印data中uuid=101810006的行的ALL值
print(data[data['uuid'] == 101810006])

