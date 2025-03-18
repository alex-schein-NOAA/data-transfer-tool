#%%

# might just be better to take the ideas from RRFS code (i.e. AWS interfacing, maybe object-oriented) and write own code

# Step 1: establish master list of filenames (possible to scrape from AWS?)
    # Careful of date ranges if doing 2+ datasets, e.g. URMA and HRRR, need to take only shared dates, but this might just be fine to do manually
# Step 2: from this master date list, generate appropriate list of filenames
    # This is unnecessary if can just fetch list of names from AWS and subset those to only what's needed
# Step 3: loop over filename list, do the following
    # Fetch from appropriate AWS source
        # Might include switch statement or different functions (if in a class) for HRRR/URMA/else
    # ONLY IF THIS SAVES SIGNIFICANT STORAGE SPACE
    # IF IT DOESN'T, ONLY HAVE A FETCHER FUNC AND THEN LOOP OVER ALL DOWNLOADED FILES AFTERWARDS
        # Subset down to 2m temp and relevant spatial vars
        # Spatially restrict this to whatever domain (have as input arg)
            # If doing CO, need to establish target region, if not the whole state (eastern CO not interesting...) but whatever domain, make sure to sample a bit outside of it to avoid edge fringing issue in actual domain of interest
        # Delete original file to save space (no point in caching, for what I'm doing)

#%%

### HERBIE TESTING

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

H = Herbie("2024-01-01 06:00", model="hrrr", fxx=6, save_dir=download_path)
#myFile

## DOESN'T WORK - downloads a 0kb file, Panoply says "authentication credentials not accepted"
#H.download(r":TMP:surface", verbose=True)

## BUT JAN 02 ONWARDS WORKS FINE???
# doesn't look like there's any difference between the files on AWS...
# H2 = Herbie('2024-01-02 06:00', model='hrrr', fxx=6, save_dir=download_path)
# H2.download(r":TMP:surface", verbose=True)

#%% test loop over all January 2024 
## Seems to work fine except for jan 01

date_strs = ['2024-01-'+str(i).zfill(2)+' 06:00' for i in range(1,32)]

for i, datestr in enumerate(date_strs):
    H = Herbie(datestr, model='hrrr', fxx=6, save_dir=download_path)
    H.download(r":TMP:surface", verbose=False)

#%%
ds = H.xarray(r":TMP:surface")
#%% plot/subsampling testing

#ds.t.plot(cmap=cm.coolwarm)

#not the greatest but it is somewhat flexible
min_lon = 360-109
max_lon = 360-102
min_lat = 37
max_lat = 41

subregion = ds.where((ds.latitude>=min_lat)&(ds.latitude<=max_lat)&(ds.longitude>=min_lon)&(ds.longitude<=max_lon), drop=True)

plt.contourf(subregion.longitude.data, subregion.latitude.data, subregion.t.data, cmap=cm.coolwarm)

#subregion.t.plot(cmap=cm.coolwarm)


#%% terrain height (really surface geopotential) testing

H2 = Herbie("2024-01-02 06:00", model="hrrr", fxx=6, save_dir=download_path)
ds2 = H2.xarray(r':HGT:surface')

subregion2 = ds2.where((ds2.latitude>=min_lat)&(ds2.latitude<=max_lat)&(ds2.longitude>=min_lon)&(ds2.longitude<=max_lon), drop=True)
#subregion2.orog.plot(cmap=cm.jet)

### xarray seems to have issues with drop=True, where it kills all the data (makes it nan) BUT inbuilt plot function works ok? makes me think it goes back up to the original object...

#lvls = np.linspace(np.min(subregion2.orog.data), np.max(subregion2.orog.data), num=50)
#plt.contourf(subregion2.longitude.data, subregion2.latitude.data, subregion2.orog.data, cmap=cm.jet, levels=lvls)

