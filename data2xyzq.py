import pandas as pd
#fileIN="EGMS_L3_E43N22_100km_E_2018_2022_1/EGMS_L3_E43N22_100km_E_2018_2022_1.csv"
fileIN_1="U/EGMS_L3_E42N21_100km_U_2018_2022_1/EGMS_L3_E42N21_100km_U_2018_2022_1.csv"
fileIN_2="U/EGMS_L3_E43N21_100km_U_2018_2022_1/EGMS_L3_E43N21_100km_U_2018_2022_1.csv"
fileIN_3="U/EGMS_L3_E43N22_100km_U_2018_2022_1/EGMS_L3_E43N22_100km_U_2018_2022_1.csv"
fileIN_4="U/EGMS_L3_E44N22_100km_U_2018_2022_1/EGMS_L3_E44N22_100km_U_2018_2022_1.csv"

PA="9.696/42.617"
PB="21.0/47.343"
region_map = [6, 22,41, 48]

fileOUT="OUT.csv" # more infor of format: https://docs.generic-mapping-tools.org/6.5/project.html

Plot = 1  # 0:No plot the figure

# read csv file, more infor of format: https://land.copernicus.eu/en/products/european-ground-motion-service
df1 = pd.read_csv(fileIN_1)
df2 = pd.read_csv(fileIN_2)
df3 = pd.read_csv(fileIN_3)
df4 = pd.read_csv(fileIN_3)
df = pd.concat([df1, df2, df3, df4], ignore_index=True)
print(df.head())

# ----------------------------------------------------------------------------
# ETRS89-LAEA转经纬度
from pyproj import Proj, transform
etrs89_laea = Proj(init='epsg:3035')
wgs84 = Proj(init='epsg:4326')
x_laea, y_laea = df['easting'], df['northing']
df['lon'], df['lat'] = transform(etrs89_laea, wgs84, x_laea, y_laea)

# 提取指定的三列数据（假设列名为 'column1', 'column2', 'column3'）
columns_to_extract = ['lon', 'lat', 'mean_velocity']
df_selected = df[columns_to_extract]

# ----------------------------------------------------------------------------
# 提取数据
import pygmt
# gmt project $file_xyzv -C$PxA/$PyA -E$PxB/$PyB -Fxyzpqrs -W-$Width/$Width -Lw -Q
track_df = pygmt.project(
    data=df_selected,
    center=PA,  # Start point 
    endpoint=PB,  # End point 
    unit=True,  #  Set units for p,q to km.  
    # convention="xyzpqrs",  
    # length="w"
)
track_df.columns = ['lon', 'lat', 'mean_velocity','p', 'q', 'r', 's']
# 将提取的数据保存到新的CSV文件
# columns_to_extract = ['lon', 'lat', 'mean_velocity', 'q']
# df_columns_to_extract = track_df[columns_to_extract]
track_df.to_csv(fileOUT, index=False)
# 显示前几行数据
print(track_df.head())

'''
# 将提取的数据保存到新的CSV文件
df_selected.to_csv('EGMS_L3_E43N22_100km_U_2018_2022_1/selected_file.csv', index=False)
# 显示前几行数据
print(df_selected.head())
'''


# ----------------------------------------------------------------------------
# Step 2
if Plot == 0:
    print("Plot is 0, no plotting the figure.")
    exit()  # 终止代码执行
else:
    print("A is not 1, continuing the code.")

# region_map = [df['lon'].min(), df['lon'].max(),df['lat'].min(), df['lat'].max()]


fig = pygmt.Figure()
fig.basemap(region=region_map, projection="M12c", frame="af",)

grid_map = pygmt.datasets.load_earth_relief(resolution="01m",region=region_map,)
fig.grdimage(grid=grid_map, cmap="oleron")

# Add a colorbar for the elevation
fig.colorbar(
    position="jBR+o0.7c/0.8c+h+w5c/0.3c+ml",
    box="+gwhite@30+p0.8p,black",
    frame=["x+lElevation", "y+lm"],
)


fig.plot(x=df['lon'], y=df['lat'], style="s.01c", fill="black")

# Choose a survey line
track_df = pygmt.project(
    data=df_selected,
    center=PA,  # Start point 
    endpoint=PB,  # End point 
    generate=0.1
)
Profile = pygmt.project(center=PA, endpoint=PB, generate=10)
fig.plot(x=Profile.r, y=Profile.s, pen="1p,red,dashed")

fig.savefig('Map.pdf')
# fig.show()
