from herbie import Herbie
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#%%
download_path = Path(r'C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads')
#%%

#urma = Herbie("2024-06-11 00:00", model="urma").xarray(verbose=True)

H = Herbie("2024-01-01 00:00", model="urma", save_dir=download_path, verbose=False)
H.download()

urma = H.xarray()[3] #[3] is where t2m is stored
urma_t2m = urma['t2m']

#%%

#not the greatest but it is somewhat flexible
min_lon = 360-109
max_lon = 360-102
min_lat = 37
max_lat = 41

#produces NaNs along edges, as the data projection is NOT rectangular, i.e. lat/lon indices change!
subregion = urma_t2m.where((urma_t2m.latitude>=min_lat)&(urma_t2m.latitude<=max_lat)&(urma_t2m.longitude>=min_lon)&(urma_t2m.longitude<=max_lon), drop=True)

#fix the NaNs with fill value. Using -1 for temp (unphysical for Kelvin). NEED TO WORK OUT HOW TO DEAL WITH THIS FOR ML...
#for whatever reason, fillna() in place doesn't actually save the data
subregion = subregion.fillna(-999)

subregion.to_netcdf(path=r'C:\Users\alex.schein\Test code and files\Test files\test_subregion.nc', format="NETCDF4")



#%%

min_t2m = np.min(np.abs(subregion.data))
max_t2m = np.max(subregion.data)
epsilon = 3

lvls = np.linspace(min_t2m-epsilon, max_t2m+epsilon, 40)


subregion.plot(cmap=cm.coolwarm, levels=lvls)