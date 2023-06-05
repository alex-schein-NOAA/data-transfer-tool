import xarray as xr
import cartopy
from RFFS import *

print(RFFS.get_file_from_storage())
# ds = get_file_from_storage('2023-05-24', 19, 6)
# path = 'model_output/2023-05-24/19/rrfs.t19z.natlev.f006.conus_3km.grib2'
# ds = xr.open_dataset(path, engine='pynio')
# print(ds)