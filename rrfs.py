import xarray as xr
from S3 import s3
from Cache import cache

#Receive variable from somewhere else
cache_name="store"
bucket = "noaa-rrfs-pds"

#Class that manages rrfs model output files
class Rrfs:

    def __init__(self):
        self.cache = cache.cache(cache_name)
        self.s3_connection = s3.s3(bucket)

    #Input: 
    # date_time : pd Timestamp object, 
    # initialization_date : int, 
    # forecast_hours : [int] | int 

    #Output: 
    # xr : xarray dataset 
    def fetch_model_forecasts(self, initialization_date, forecast_hours):
        
        #Stores forecast dataframes in a list
        forecasts = []

        #If the only one forecast hour was requested
        if type(forecast_hours) == int:
            forecast_hour = forecast_hours
            return self.fetch_model_forecast(initialization_date, forecast_hour)

        #If the forecasts hours are a list
        elif type(forecast_hours) == list:
            #Opens each forecast and appends to list
            for hour in forecast_hours:
                forecasts.append(self.fetch_model_forecast(initialization_date, hour))
            
            #Makes the list into a data frame with a time dimension
            xr = self.make_data_frame(forecasts)
            return xr 

        else :
            raise Exception(f'{type(forecast_hours)} as forecast hours is not supported')
        

    #Input: date_time : pd Timestamp object, initialization_date:  forecast_hour : int 
    #Output: xr : xarray dataset 
    def fetch_model_output(self, initialization_date, forecast_hour):

        init_hour_str = initialization_date.strftime("%H")      #S3 init hour
        init_date_str = initialization_date.strftime("%Y%m%d")  #S3 init_date 

        file_name = self.make_model_file_name(init_hour_str,forecast_hour)

        #Checks cache for file
        if self.cache.check_cache(file_name, init_date_str, init_hour_str):
            #Returns file if in cache
            return self.cache.fetch(file_name, init_date_str, init_hour_str)
        
        #Otherwise downloads file from bucket and writes to cache
        else :
            
            # Path and file name for the cache level
            download_path = self.cache.get_download_path()
            # Cache file name
            cfile_name = self.cache.get_cfile_name(file_name, init_date_str, init_hour_str)
            # S3 bucket file name
            try :
                object_name = self.make_s3_object_name(file_name, init_date_str, init_hour_str)
                #Downloads file from bucket and writes it to the download path with c_file_name as filename
                self.s3_connection.download_file(object_name, download_path, cfile_name)
                # self.cache.put(file_name, file_content, init_date_str, init_hour_str)
                #Returns cached data as xarray dataset
                return self.cache.fetch(file_name, init_date_str, init_hour_str)
            except: 
                return  

    
    #Helper functions:
    #Creates the rrfs file name
    #Follows the convention of the bucket
    def make_model_file_name(self,initialization_hour, forecast_hour, output_type="nat"):
        f_hour = str(forecast_hour) if forecast_hour >= 10 else f'0{forecast_hour}'
        file_name = f'rrfs.t{initialization_hour}z.{output_type}lev.f0{f_hour}.conus_3km.grib2'
        return file_name
    
    #Creates object name for file in bucket
    def make_s3_object_name(self, file_name, date_time_str, init_hour_str):
        date_time = date_time_str.split("-")
        date_time = ''.join(map(str, date_time))
        return f"rrfs_a/rrfs_a.{date_time}/{init_hour_str}/control/{file_name}"

    def make_dataframe(self,forecasts):
        df = xr.concat(forecasts)
        return df 
    