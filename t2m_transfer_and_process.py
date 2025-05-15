from herbie import Herbie
from pathlib import Path
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#%%
download_path = r'C:\Users\alex.schein\Test code and files\Test files\Herbie_downloads'
#%%

#urma = Herbie("2024-06-11 00:00", model="urma").xarray(verbose=True)

# H = Herbie("2024-01-01 00:00", model="urma", save_dir=download_path, verbose=False)

H = Herbie("2024-01-01 00:00", model="urma", save_dir=download_path, verbose=False)
try:
    inventory = H.inventory()
    print(f"")
except:
    print(f"has no inventory file")
    
# H.download()

# urma = H.xarray()[3] #[3] is where t2m is stored
# urma_t2m = urma['t2m']


#%%

#testing which URMA files have idx files
#rerunning this is expensive! don't do it...

# start_date = date(2014,7,30)
# end_date = date(2025,3,20)
# num_days = end_date-start_date

# with open(download_path+'\\'+'does_URMA_file_have_idx.txt', 'w') as file:
#     for i in range(num_days.days +1):
#         datestr = date.strftime(start_date + timedelta(days=i), "%Y-%m-%d")
#         # print(f"{datestr}")
#         H_urma = Herbie(f'{datestr} 00:00', model='urma', save_dir=download_path, verbose=False)
#         try:
#             inventory = H_urma.inventory()
#             print(f"!!! {datestr} has an inventory!")
#             file.write(f"YES {datestr} \n")
#         except:
#             print(f"{datestr} has no inventory")
#             file.write(f"NO {datestr} \n")

#%%

#not the greatest but it is somewhat flexible
min_lon = 360-109
max_lon = 360-102
min_lat = 37
max_lat = 41

#produces NaNs along edges, as the data projection is NOT rectangular, i.e. lat/lon indices change!
# subregion = urma_t2m.where((urma_t2m.latitude>=min_lat)&(urma_t2m.latitude<=max_lat)&(urma_t2m.longitude>=min_lon)&(urma_t2m.longitude<=max_lon), drop=True)

#fix the NaNs with fill value. Using -1 for temp (unphysical for Kelvin). NEED TO WORK OUT HOW TO DEAL WITH THIS FOR ML...
#for whatever reason, fillna() in place doesn't actually save the data
# subregion = subregion.fillna(-999)

# subregion.to_netcdf(path=r'C:\Users\alex.schein\Test code and files\Test files\test_subregion.nc', format="NETCDF4")



#%%

# min_t2m = np.min(np.abs(subregion.data))
# max_t2m = np.max(subregion.data)
# epsilon = 3

# lvls = np.linspace(min_t2m-epsilon, max_t2m+epsilon, 40)


# subregion.plot(cmap=cm.coolwarm, levels=lvls)