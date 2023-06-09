# rrfs

rrfs_api:

The rrfs_api python package was created to simplify the download and management of the Rapid Refresh Forecast System (RRFS) model output files. 

The package exposes a function that fetches RRFS model output files for a given initialization time and forecast hour. 
The function returns the requested model output file as an xarray dataset. 

When a forecast is requested, rrfs_api checks the cache to see if the requested forecast has already been fetched. If it's not in the cache
the package downloads the model output, stores it in the cache and returns the given forecast. 

Notes:
    -Downlading a single model output file takes about 2-3 min with good internet. 
    -Each model output is about ~1 gb of data. Be mindful when downloading many model outputs. 
    -The model files are stored inside the folder "./rrfs_api/store/..". 
    -Be mindful of the memory usage and delete the cache every once in a while

Setting up:

    TODO: Figure this out
    To run the notebook, create the enviroment from the enviroment.yml file using conda. Run the command

    conda env create -f environment.yml

Function:
    Input: 
        
    fetch_model_forecast(initialization_date, forecast_hour)

        -initialization_date : pd.Timestamp 
        -forecast_hour : int 
    
    output :

        -ds : xarray dataset

Usage:

    from RRFS import rrfs
    r = rrfs.rrfs()

    #Forecast initialization date at 2023-05-23 1:00:00 
    initialization_date = pd.Datetime(year=2023, month=5, day=23, hour=1)
    forecast_hour = 6

    #Returns model forecast at datetime 2023-05-23 7:00:00
    r.fetch_model_output(initialization_date, forecast_hour)


TODOS:
    -Restructure file system structure to only have 1 folder and a datetime-initialization hour specific name for each file
    -Make module that evaluates memory usage and monitors usage. Maybe it can delete least used files to save memory
    -Make new cache module that uses an sqlite database 
    