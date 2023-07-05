import pandas as pd
import xarray as xr
from S3 import s3
from Cache import cache

cache_name = "store"
bucket = "noaa-mrms-pds"
zipped = True

class Mrms:

    def __init__(self):
        self.cache = cache.cache(cache_name)
        self.s3_connection = s3.s3(bucket)

    
    def fetch_mrms_data(self,date_time):
        # init_hour_str = date_time.strftime("%H")      #S3 init hour
        date_time_str = date_time.strftime("%Y%m%d")  #S3 init_date 
        file_name = self.make_model_file_name(date_time_str=date_time_str,date_time=date_time)

        #Checks cache for file
        if self.cache.check_cache(file_name, date_time_str,):
            #Returns file if in cache
            return self.cache.fetch( file_name, date_time_str, zipped=zipped)
        
        #Otherwise downloads file from bucket and writes to cache
        else :
            
            #Path and file name for the cache level
            download_path = self.cache.get_download_path()
            #Cache file name
            cfile_name = self.cache.get_cfile_name(file_name, date_time_str)
            #S3 bucket file name
            object_name = self.make_s3_object_name(file_name, date_time_str)
            #Downloads file from bucket and writes it to the download path with c_file_name as filename
            self.s3_connection.download_file(object_name, download_path, cfile_name)
            
            
            #Returns cached data as xarray dataset
            return self.cache.fetch(file_name, date_time_str, zipped=zipped)

    
        
    #Helper functions:
    #Creates the mrms file name
    #Follows the convention of the bucket
    def make_model_file_name(self,date_time_str, date_time,mrms_product='MergedReflectivityComposite_00.50'):

        time_of_sounding = self.get_time_of_sounding(date_time_str, date_time ,mrms_product)
        file_name = f'MRMS_{mrms_product}_{date_time_str}-{time_of_sounding}.grib2.gz'
        return file_name
    
    #Creates object name for file in bucket
    def make_s3_object_name(self, file_name, date_time_str, mrms_product='MergedReflectivityComposite_00.50'):
        date_time = date_time_str.split("-")
        date_time = ''.join(map(str, date_time))
        return f"CONUS/{mrms_product}/{date_time_str}/{file_name}"
    
    #Used as helper function to create the minutes corresponding to the correct date 
    def get_time_of_sounding(self, date_time_str, date_time, mrms_product):
        files = self.s3_connection.get_files_in_bucket(f"CONUS/{mrms_product}/{date_time_str}")

        time_stamps = []
        for file in files:
            time_stamps.append(self.get_time_stamp(file, date_time))

        time_of_sounding = self.nearest(time_stamps, date_time)
       
        return time_of_sounding.strftime("%H%M%S")
    
    #Used to convert the file name to a time stamp
    def get_time_stamp(self, file, date_time):
        file_name = file['Key']
        time_and_ext = file_name.split('-')[1]       #Hardcoded
        time = time_and_ext.split('.')[0]
        year, month, day =date_time.year, date_time.month, date_time.day
        hour, minute, second = int(time[0] + time[1]), int(time[2] + time[3]), int(time[4] + time[5])
        time_stamp = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        return time_stamp
    
    def nearest(self,items, pivot):
        return min(items, key=lambda x: abs(x - pivot))