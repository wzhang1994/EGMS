import pandas as pd
import matplotlib.pyplot as plt

# 创建数据集
data = {
    'x': [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6, 6.2, 6.4],
    'v': [192.947166334, 192.782792432, 192.864979441, 193.275912748, 192.700605306, 192.536230708, 192.28966794, 192.207480118, 191.549973364, 191.221217198, 191.87872767, 191.796539268, 191.385595514, 191.960915957, 191.303406414, 191.71435075, 191.467784497, 191.632162115, 192.017471866, 191.770906517, 193.029353112, 193.193726319, 193.111539773, 193.00372281, 192.839348813, 192.757161641, 193.250282936, 193.085909635, 193.168096343, 193.332469413, 192.618418065, 192.043104127, 192.371855645]
}

df = pd.DataFrame(data)

# 计算每段的平均值
df['segment'] = (df['x'] // 2).astype(int)
segment_avg = df.groupby('segment')['v'].mean().reset_index()

# 计算每段的标准偏差
segment_std = df.groupby('segment')['v'].std().reset_index()

# 绘制平均值和标准偏差图
fig, ax = plt.subplots()

ax.plot(data['x'], data['v'],'.')

# 绘制平均值和标准偏差
ax.plot(segment_avg['segment']*2, segment_avg['v'],'-')

ax.errorbar(segment_avg['segment']*2, segment_avg['v'], yerr=segment_std['v'], fmt='o', capsize=5, label='Average with Std Dev')

# 添加标签和标题
ax.set_xlabel('Segment')
ax.set_ylabel('Value')
ax.set_title('Segment Averages and Standard Deviations')
ax.legend()


# Filter the dataframe for x values between 0 and 1 inclusive
filtered_df = df[(df['x'] >= 0) & (df['x'] < 2)]

# Calculate the mean of the 'v' values within this range
mean_v = filtered_df['v'].mean()
ax.plot(0.5, mean_v,'r.')

print(segment_avg)
print(mean_v)

# 显示图表
plt.show()

