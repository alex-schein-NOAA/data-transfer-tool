import os
import xarray as xr 
from datetime import datetime
import pandas as pd

class cache:
    def __init__(self, cache_name):
        self.cache_name = cache_name
        self.evaluate_cache(cache_name)
        return 
    
    #Evaluates if cache exists. Otherwise it creates it
    #In the future, can return memory usage information object
    def evaluate_cache(self, cache_name):

        if os.path.exists(f"{os.getcwd()}/{cache_name}"):
            #TODO: Do stuff with the cache folder
            #      Analytics on memory usage maybe?
            return 
        else :
            #Creates cache
            self.create_cache(cache_name)
            return 

    #Creates cache folder
    def create_cache(self, cache_name):
        try :
            os.mkdir(f'{os.getcwd()}/{cache_name}')
        
        except :
            raise Exception(f"Failed to create model forecast store")
        
        return 
       
    #Checks if given forecast is in cache
    def check_cache(self,file_name, init_date_time_str, init_hour_str=False):

        #Checks file is in cache
        file = self.get_cfile_name(file_name,init_date_time_str, init_hour_str)
        download_path = self.get_download_path()
        if file in os.listdir(download_path):
            return True 
        else :
            return False
        
    #Fetches given forecast from the cache
    def fetch(self, file_name, date_time_str,init_hour_str=False):
        file = self.get_cfile_name(file_name, date_time_str, init_hour_str)
        download_path = self.get_download_path()
        return xr.open_dataset(f"{download_path}/{file}", engine="pynio")

        
    #Helper function:
    #Generates cache_file name 
    def get_cfile_name(self,file_name, init_date_time_str, init_hour_str=False):
        if init_hour_str:
            return f"{init_date_time_str}-{init_hour_str}-{file_name}"
        else :
            return f"{init_date_time_str}-{file_name}"

    
    #Eventually will be useful if cache folder location is moved
    def get_download_path(self):
        return f'{os.getcwd()}/{self.cache_name}'
