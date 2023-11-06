# filename: tesla_stock_chart.py

import pandas as pd
import matplotlib.pyplot as plt

# 获取特斯拉的股票数据
tesla_stock_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/tesla-stock-price.csv')

# 将日期列转换为日期类型
tesla_stock_data['date'] = pd.to_datetime(tesla_stock_data['date'])

# 设置日期列为索引，并根据日期升序排序
tesla_stock_data.set_index('date', inplace=True)
tesla_stock_data.sort_index(ascending=True, inplace=True)

# 绘制变化图表
plt.figure(figsize=(12, 6))
plt.plot(tesla_stock_data['close'], color='blue')
plt.title('Tesla Stock Price')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.grid(True)
plt.show()