import pandas as pd
import matplotlib.pyplot as plt

# 不使用科学计数法
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# CSV文件路径
csv_file = "D:\\202310312103.csv"  # 请替换成你的CSV文件路径

# 列名，用于选择X轴和Y轴的列
x_column = "NGFIX_LOG_FIX_RECEIVE"  # 请替换成你要用作X轴的列的名称
y_column = "ALL"  # 请替换成你要用作Y轴的列的名称

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




# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, marker='o', linestyle='-', color='b')
plt.title(f"{x_column} vs. {y_column} 折线图")
plt.xlabel(f"{x_column}")
plt.ylabel(f"{y_column}")
# 折线图显示不使用科学计数法
plt.rcParams['axes.formatter.useoffset'] = False

# 显示折线图
plt.grid(True)
plt.show()



