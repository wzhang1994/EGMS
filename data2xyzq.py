# conda activate pygmt
import pandas as pd
import glob
import pygmt

fileTopoOUT="OUT_topo.csv"

# read *.csv
csv_files = glob.glob('E/*2018_2022_1/*.csv', recursive=True)
csv_files = glob.glob('U/*2018_2022_1/*.csv', recursive=True)
fileOUT="OUT.csv" # more infor of format: https://docs.generic-mapping-tools.org/6.5/project.html

# Read all CSV files and store them into a list
dfs = [pd.read_csv(file, usecols=['easting', 'northing', 'mean_velocity']) for file in csv_files]
df = pd.concat(dfs, ignore_index=True)
print(df)

# Profile settings
PA="9.696/42.617"
PB="21.0/47.343"

PA="10.99031082816053/42.62324008933551"
PB="13.3242832934694/43.73597452591967"

region_map = [6, 22,41, 48]

Plot = 0  # 0:No plot the figure

# ----------------------------------------------------------------------------
# transfer ETRS89-LAEA to longitude and latitude
from pyproj import Proj, transform
etrs89_laea = Proj(init='epsg:3035')
wgs84 = Proj(init='epsg:4326')
x_laea, y_laea = df['easting'], df['northing']
df['lon'], df['lat'] = transform(etrs89_laea, wgs84, x_laea, y_laea)

# Extract the specified three columns of data
columns_to_extract = ['lon', 'lat', 'mean_velocity']
df_selected = df[columns_to_extract]

# ----------------------------------------------------------------------------
# Extracted by pygmt
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

# Save the extracted data to a new CSV file
track_df.to_csv(fileOUT, index=False)
print(track_df.head())


# ----------------------------------------------------------------------------
# Topography
grid_map = pygmt.datasets.load_earth_relief(
    resolution="01m",
    region=region_map,
)
track_topo = pygmt.project(
    center=PA,  # Start point 
    endpoint=PB,  # End point 
    unit=True,  #  Set units for p,q to km.  
    generate=0.1
)
track_topo = pygmt.grdtrack(
    grid=grid_map,
    points=track_topo,
    newcolname="elevation",
)
track_topo.to_csv(fileTopoOUT, index=False)




# ----------------------------------------------------------------------------
# Step 2: Plot
if Plot == 0:
    print("Plot is 0, no plotting the figure.")
    exit()  # Terminate code execution
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
