import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import pygmt
# PA="10.53/42.91"
# PB="10.86/43.80"
fileOUT="OUT.csv"
Wigth=20 #  The max distance (km) with the selected profile
# Label='Horizontal mean_velocity, mm/y'
Label='Vertical mean_velocity, mm/y'


df_all = pd.read_csv(fileOUT)
print(df_all)
# df = df_all[df_all['q'].abs() < Wigth]
df = df_all[df_all['q'].abs() < Wigth].copy()
print(df)

# 创建一个2行1列的子图结构s
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 8), sharex=True)

# 第一个子图
#scatter = axes[0].scatter(df_all['p'], df_all['q'], c=df_all['mean_velocity'], cmap='rainbow', s=1.0, vmin=-3, vmax=3) # rainbow, viridis
scatter = axes[0].scatter(df['p'], df['q'], c=df['mean_velocity'], cmap='rainbow', s=1.0, vmin=-3, vmax=3)
axes[0].axhline(y=Wigth, color='red', linestyle='--', linewidth=2, label='y = 10')
axes[0].axhline(y=-Wigth, color='red', linestyle='--', linewidth=2, label='y = 10')
colorbar = fig.colorbar(scatter, ax=axes[0])
colorbar.set_label(Label)
colorbar = fig.colorbar(scatter, ax=axes[1])
colorbar = fig.colorbar(scatter, ax=axes[2])

axes[0].set_title('Scatter Plot of All')
axes[0].set_xlabel('Distance/km')
axes[0].set_ylabel('Distance from Projection to Start/km')
axes[0].grid(True)
axes[0].set_xlim([0,240])


# 第二个子图
axes[1].scatter(df['p'], df['mean_velocity'], c='blue', s=1.0)
axes[1].set_title(f'The mean_velocity along the profile (< %.1f km)' % Wigth)

axes[1].set_xlabel('Distance/km')
axes[1].set_ylabel(Label)
axes[1].grid(True)
axes[1].set_ylim([-10,10])

plt.tight_layout()



# 第三个子图s

# Calculate the mean of each segment with a length of 1
segment_length = 2

# 计算每段的平均值
df['segment'] = (df['p'] // segment_length).astype(int)
segment_avg = df.groupby('segment')['mean_velocity'].mean().reset_index()
# 计算每段的标准偏差
segment_std = df.groupby('segment')['mean_velocity'].std().reset_index()


print('******1*********')
#axes[2].scatter(segment_avg['segment']*segment_length, segment_avg['mean_velocity'], c='blue', s=2.0)
axes[2].errorbar(segment_avg['segment']*segment_length, segment_avg['mean_velocity'], yerr=segment_std['mean_velocity'], fmt='b.', capsize=5, ecolor='r',elinewidth=0.4,label='Average with Std Dev')
print('******2*********')
axes[2].set_title(f'The mean_velocity along the profile (< %.1f km)' % Wigth)
axes[2].set_xlabel('Distance/km')
axes[2].set_ylabel(Label)
axes[2].grid(True)



plt.savefig('Profile.png')
# plt.savefig("Profile.pdf", dpi=150)
# plt.show()
