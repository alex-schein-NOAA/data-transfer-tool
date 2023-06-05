import os
import xarray as xr

def make_model_file_name(initialization_hour, forecast_hour):
    print(initialization_hour)
    file_name = f'rrfs.t{initialization_hour}z.natlev.f00{forecast_hour}.conus_3km.grib2'
    return file_name

def get_file_from_store(date_time, initialization_hour, forecast_hour):
    init_hour_str = str(initializatioxn_hour)
    f_hour_str = str(forecast_hour)
    #TODO: Figure out how to convert this to string
    date_time_str = date_time
    #Checks if file is in date time file folder
    if date_time_str in os.listdir("../model_output"):
        #Check if folder for model date exists
        if init_hour_str in os.listdir(f"../model_output/{date_time_str}"):
            file_name = make_model_file_name(initialization_hour,forecast_hour)
            if file_name in os.listdir(f"../model_output/{date_time_str}/{init_hour_str}"):
                #If file has been downloaded, return dataset
                return xr.open_dataset(f"../model_output/{date_time_str}/{init_hour_str}/{file_name}", engine='pynio')
            else :
                #TODO: 
                #Forecast time has not yet been used
                #Fetch file
                #return xarray dataset
                raise Exception("Download model file")
                return 
        else :
            #TODO:
            #Model output with that initialization hour has not been used yet
            #Create folder for initialization hour 
            #Fetch file from s3 bucket and put in folder
            #Return xarray dataset 
            raise Exception("Download model file")
            return 
    #If file is not in date time file folder 
    else :
        #TODO:
        #Model out with for that date has not been used yet 
        #Create folder for date time object
        #Create folder for initialization hour
        #Fetch file from s3 bucket and put in folder 
        #Return xarray dataset
        raise Exception("Download model file")
        return
            
    return 


#TODO: Implement
def create_folder_structure(level, date_time, ):
    if level == 'd':
        os.makedir(f"../model_output/{date_time}")

#TODO: Implement once credentials are figured out
def fetch_model_data(file_name):
    #Use s3 api to download file from bucket
    return 
