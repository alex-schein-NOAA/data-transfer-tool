import os
import xarray as xr
from .S3 import s3
from .Cache import cache

#Receive variable from somewhere else
cache_name="cache"
error_message = "Model file missing from cache. Please download model file"
bucket = "noaa-rrfs-pds"

class rrfs:

    def __init__(self):
        cache = cache(cache_name)
        s3_connection = s3(bucket)
        

    def make_model_file_name(self,initialization_hour, forecast_hour):
        file_name = f'rrfs.t{initialization_hour}z.natlev.f00{forecast_hour}.conus_3km.grib2'
        return file_name

    # Input:
    #     date_time : DateTime object
    #     initialization_hour : int
    #     forecast_hour : int 
    #Output:
        # xr : xarray dataset 
    def fetch_file(self,date_time, initialization_hour, forecast_hour):


        init_hour_str = str(initialization_hour)
        f_hour_str = str(forecast_hour)
        #TODO: Figure out how to convert this to string
        date_time_str = date_time

        file_name = self.make_model_file_name(initialization_hour,forecast_hour)

        if file_name in os.listdir(f"./{cache_name}/{date_time_str}/{init_hour_str}"):
            #If file has been downloaded, return dataset
            return xr.open_dataset(f"./{cache_name}/{date_time_str}/{init_hour_str}/{file_name}", engine='pynio')
        else :
            #TODO: Call S3 method to download file
            #TODO: Figure out how to download file to correct path
            raise Exception(error_message)


