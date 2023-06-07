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

        if os.path.exists(f"{os.getcwd()}/RRFS/{cache_name}"):
            #TODO: Do stuff with the cache folder
            #      Analytics on memory usage maybe?
            return 
        else :
            #Creates cache
            self.create_cache(cache_name)
            return 

    #Creates cache filesystem structure
    def create_cache(self, cache_name):
        print("Creating model forecast store")
        dates_array = self.dates()
        #TODO: Put in an import 
        init_hour_array = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                           '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
                           '22', '23']
        
        #TODO: Figure out how to programatically create path
        try :
            #Creates parent folder
            os.mkdir(f'{os.getcwd()}/RRFS/{cache_name}')
            #Creates folder for every date in the date_array
            for date in dates_array:
                os.mkdir(f'{os.getcwd()}/RRFS/{cache_name}/{date}')
                #Creates folder for every initialization hour in each date folder
                for init_hour in init_hour_array:
                    os.mkdir(f'{os.getcwd()}/RRFS/{cache_name}/{date}/{init_hour}')
        except :
            raise Exception(f"Failed to create model forecast store")
        
        return 
    
    def get_path(self,date_time_str, init_hour_str, file_name):
        return f"{os.getcwd()}/RRFS/{self.cache_name}/{date_time_str}/{init_hour_str}"

    #Helper function:
    #Checks if given forecast is in cache
    def check_cache(self,date_time_str, init_hour_str, file_name):
        #TODO: Figure out how to programatically create path

        #Checks file is in cache
        file_path = self.get_path(date_time_str, init_hour_str, file_name)
        if file_name in os.listdir(file_path):
            return True 
        else :
            return False
    
    #Fetches given forecast from the cache
    def fetch(self, date_time_str, init_hour_str, file_name):
        #TODO: Figure out how to programatically create path
        return xr.open_dataset(f"{os.getcwd()}/RRFS/{self.cache_name}/{date_time_str}/{init_hour_str}/{file_name}", engine="pynio")

    #Helper function
    #Generates all the dates in specified range
    def dates(self, date_start=datetime(2023,5,1), days=30):
        date_list = pd.date_range(date_start, periods=days).to_list()
        return [d.strftime("%Y-%m-%d") for d in date_list]