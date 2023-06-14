import os
import pandas as pd
import xarray as xr
from .S3 import s3
from .Cache import cache

#Receive variable from somewhere else
cache_name="store"
bucket = "noaa-rrfs-pds"

#Class that manages rrfs model output files
class Rrfs:

    def __init__(self):
        self.cache = cache.cache(cache_name)
        self.s3_connection = s3.s3(bucket)

        
    #Input: date_time : pd Timestamp object, initialization_date:  forecast_hour : int 
    #Output: xr : xarray dataset 
    def fetch_model_output(self, initialization_date, forecast_hour):

        init_hour_str = initialization_date.strftime("%H")      #S3 init hour
        init_date_str = initialization_date.strftime("%Y%m%d")  #S3 init_date 

        file_name = self.make_model_file_name(init_hour_str,forecast_hour)

        #Checks cache for file
        if self.cache.check_cache(init_date_str, init_hour_str,file_name):
            #Returns file if in cache
            return self.cache.fetch(init_date_str, init_hour_str, file_name)
        
        #Otherwise downloads file from bucket and writes to cache
        else :
            
            #Path and file name for the cache level
            download_path = self.cache.get_download_path()
            #Cache file name
            cfile_name = self.cache.get_cfile_name(init_date_str, init_hour_str,file_name)
            
            #Downloads file from bucket and writes it to the download path with c_file_name as filename
            self.s3_connection.download_file(init_date_str, init_hour_str, file_name, download_path, cfile_name)
            
            #Returns cached data as xarray dataset
            return self.cache.fetch(init_date_str, init_hour_str, file_name)

    
    #Helper functions:
    #Creates the rrfs file name
    #Follows the convention of the bucket
    def make_model_file_name(self,initialization_hour, forecast_hour, output_type="nat"):
        f_hour = str(forecast_hour) if forecast_hour >= 10 else f'0{forecast_hour}'
        file_name = f'rrfs.t{initialization_hour}z.{output_type}lev.f0{f_hour}.conus_3km.grib2'
        return file_name
    
