import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import pygmt
Wigth=20 		#  The max distance (km) with the selected profile
segment_length = 2 	# Calculate the mean of each segment with a length

# figure
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6, 8), sharex=True)
fig.suptitle('Northern Apennines', fontsize=14)
# axes[0].set_xlim([-100,300])
axes[0].set_xlim([-50,250])

# ———————— subfigure 1
fileOUT="OUT_E.csv"
Label='$V_x\ (mm/y)$'
df_all = pd.read_csv(fileOUT)
df = df_all[df_all['q'].abs() < Wigth].copy()
# Calculate the mean value and standard deviation of each segment
df['segment'] = (df['p'] // segment_length).astype(int)
segment_avg = df.groupby('segment')['mean_velocity'].mean().reset_index()
segment_std = df.groupby('segment')['mean_velocity'].std().reset_index()

Subfigure=0
# axes[Subfigure].scatter(df['p'], df['mean_velocity'], c='green', s=0.5)
axes[Subfigure].errorbar(segment_avg['segment']*segment_length, segment_avg['mean_velocity'], yerr=segment_std['mean_velocity'], fmt='b.', capsize=5, ecolor='r',elinewidth=0.4,label='Average with Std Dev')

axes[Subfigure].set_title(f'Horizontal mean_velocity along the profile (< %.1f km)' % Wigth)
# axes[Subfigure].set_xlabel('Distance/km')
axes[Subfigure].set_ylabel(Label)
axes[Subfigure].grid(True)
axes[Subfigure].set_ylim([-6,6])

# ———————— subfigure 2
fileOUT="OUT_U.csv"
Label='$V_z\ (mm/y)$'
df_all = pd.read_csv(fileOUT)
df = df_all[df_all['q'].abs() < Wigth].copy()
# Calculate the mean value and standard deviation of each segment
df['segment'] = (df['p'] // segment_length).astype(int)
segment_avg = df.groupby('segment')['mean_velocity'].mean().reset_index()
segment_std = df.groupby('segment')['mean_velocity'].std().reset_index()

Subfigure=1
# axes[Subfigure].scatter(df['p'], df['mean_velocity'], c='blue', s=1.0)
axes[Subfigure].errorbar(segment_avg['segment']*segment_length, segment_avg['mean_velocity'], yerr=segment_std['mean_velocity'], fmt='b.', capsize=5, ecolor='r',elinewidth=0.4,label='Average with Std Dev')

axes[Subfigure].set_title(f'Vertical mean_velocity along the profile (< %.1f km)' % Wigth)
# axes[Subfigure].set_xlabel('Distance/km')
axes[Subfigure].set_ylabel(Label)
axes[Subfigure].grid(True)
axes[Subfigure].set_ylim([-4,4])



# ———————— subfigure 3
fileTopoOUT="OUT_topo.csv"
Label='$Topography\ (km)$'
df = pd.read_csv(fileTopoOUT)

Subfigure=2
axes[Subfigure].plot(df['p'], df['elevation'])
axes[Subfigure].set_title('Elevation')
axes[Subfigure].set_xlabel('Distance/km')
axes[Subfigure].set_ylabel(Label)
axes[Subfigure].grid(True)


plt.savefig('Profile_NA.png')
# plt.savefig("Profile_NA.pdf", dpi=150)
# plt.show()
