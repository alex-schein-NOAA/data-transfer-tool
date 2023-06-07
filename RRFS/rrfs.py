import os
import xarray as xr
from .S3 import s3
from .Cache import cache

#Receive variable from somewhere else
cache_name="store"
error_message = "Model file missing from cache. Please download model file"
bucket = "noaa-rrfs-pds"

#Class that manages rrfs model output files
class rrfs:

    def __init__(self):
        self.cache = cache.cache(cache_name)
        self.s3_connection = s3.s3(bucket)

        
    #Input: date_time : pd Timestamp object, initialization_hour : int, forecast_hour : int 
    #Output: xr : xarray dataset 
    def fetch_model_forecast(self,date_time_str, initialization_hour, forecast_hour):

        init_hour_str = str(initialization_hour)
        f_hour_str = str(forecast_hour)

        file_name = self.make_model_file_name(initialization_hour,forecast_hour)


        if self.cache.check_cache(date_time_str, init_hour_str, file_name):
            return self.cache.fetch(date_time_str, init_hour_str, file_name)
        else :

            download_path = self.cache.get_path(date_time_str, init_hour_str, file_name)
            self.s3_connection.download_file(date_time_str, init_hour_str, file_name, download_path)
            return self.cache.fetch(date_time_str, init_hour_str, file_name)

    
    def make_model_file_name(self,initialization_hour, forecast_hour, output_type="nat"):
        file_name = f'rrfs.t{initialization_hour}z.{output_type}lev.f00{forecast_hour}.conus_3km.grib2'
        return file_name