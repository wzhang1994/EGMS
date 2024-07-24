import matplotlib.pyplot as plt
import pandas as pd
import pygmt
# PA="10.53/42.91"
# PB="10.86/43.80"
fileOUT="OUT.csv"
Wigth=10 #  The max distance with the selected profile

df = pd.read_csv(fileOUT)
df.plot(kind='scatter', x='p', y='mean_velocity', figsize=(10, 6))
plt.xlabel('Distance/km')
plt.ylabel('mean_velocity')
plt.title('All')
plt.show()


filtered_df = df[df['q'].abs() < Wigth]
filtered_df.plot(kind='scatter', x='p', y='mean_velocity', figsize=(10, 6))
plt.xlabel('Distance/km')
plt.ylabel('mean_velocity')
plt.title('10')
plt.show()
