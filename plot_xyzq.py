import matplotlib.pyplot as plt
import pandas as pd
import pygmt
# PA="10.53/42.91"
# PB="10.86/43.80"
fileOUT="OUT.csv"
Wigth=25 #  The max distance (km) with the selected profile



df_all = pd.read_csv(fileOUT)
df = df_all[df_all['q'].abs() < Wigth]
# 创建一个2行1列的子图结构
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

# 第一个子图
scatter = axes[0].scatter(df_all['p'], df_all['q'], c=df_all['mean_velocity'], cmap='rainbow', s=1.0, vmin=-20, vmax=20) # rainbow, viridis
axes[0].axhline(y=Wigth, color='red', linestyle='--', linewidth=2, label='y = 10')
axes[0].axhline(y=-Wigth, color='red', linestyle='--', linewidth=2, label='y = 10')
colorbar = fig.colorbar(scatter, ax=axes[0])
colorbar = fig.colorbar(scatter, ax=axes[1])
colorbar.set_label('mean_velocity, mm/y')
axes[0].set_title('Scatter Plot of All')
axes[0].set_xlabel('Distance/km')
axes[0].set_ylabel('Distance from Projection to Start/km')
axes[0].grid(True)



# 第二个子图
axes[1].scatter(df['p'], df['mean_velocity'], c='blue', s=1.0)
axes[1].set_title(f'The mean_velocity along the profile (< %.1f km)' % Wigth)

axes[1].set_xlabel('Distance/km')
axes[1].set_ylabel('mean_velocity')
axes[1].grid(True)

plt.tight_layout()

plt.savefig('Profile.png')
# plt.show()
