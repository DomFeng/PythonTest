import pandas as pd
import matplotlib.pyplot as plt

# 不使用科学计数法
# pd.set_option('display.float_format', lambda x: '%.3f' % x)

# CSV文件路径
csv_file = "E:\\性能测试\\长城证券日志\\第三批性能测试\\撮合\\part-00000-bb7834c7-f604-4721-b0b5-6f1d3fd09725-c000.csv"  # 请替换成你的CSV文件路径

# 列名，用于选择X轴和Y轴的列
x_column = "API_GATE_LOG_SEND"  # 请替换成你要用作X轴的列的名称
y_column = "ALL_UP"  # 请替换成你要用作Y轴的列的名称

# 读取CSV文件
data = pd.read_csv(csv_file)

# 提取X轴和Y轴数据
x_data = data[x_column]
y_data = data[y_column]

# 将x_data倒序排列
x_data = x_data[::-1]

# 打印y_data有多少个值
print(f"x_data has {len(x_data)} values.")
print(f"y_data has {len(y_data)} values.")

# y_data不使用科学计数法
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# 折线图显示不使用科学计数法
# plt.rcParams['axes.formatter.useoffset'] = False

# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
plt.title(f"{x_column} vs. {y_column} 折线图")
plt.xlabel(f"{x_column}")
plt.ylabel(f"{y_column}")


# 显示折线图
plt.grid(True)
plt.show()



