# rrfs

rrfs_api:

The rrfs_api python package was created to simplify the download and management of the Rapid Refresh Forecast System (RRFS) model output files. 
The RRFS is a prototype model that is set to be operational in early 2024. Every hour, the model produces a 24 hour forecast (1 forecast for every hour) over the entire continental US. Each forecast produced by the model at any hour is about 1.5gb. These files can be accesed via Amazon AWS at the following link (link). In order to use the model output files, one must go to AWS, download the file to somewhere on the computer and load into your favorite programming language. Downloading the model outputs is a tedious task. Managing multiple model output files can get complicated when comparing different outputs. This package was created to solve these two problems.

To solve the downloading problem, the rrfs_api uses the boto3 api to download the model outputs from the the bucket containing them. To solve the management of model outputs, the rrfs_api uses a file system cache. When a specific model output is requested, the rrfs_api will check the cache to see if that model output had been previously requested and return it as an xarray dataset. Otherwise, the rrfs_api will fetch the file from the bucket, store it in the cache and then return the data as an xarray dataset. 

This can be achieved with the method fetch_model_output. For the model outputs that are being considered, they can be uniquely identified by a combination of initialization date and hour, and forecast hour. These are the two inputs we pass to the fetch_model_output method and get an xarray dataset with the output. This method can be fast (if the model has been cached) or slow (if it needs to be downloaded). 

This package is in its initial stages. It has various problems that need to be addressed and features that need to be added. One problem is the overly complicated file system structure. This was chosen to mirror the bucket, but it doesn't scale well when considering many different dates. A simpler solution is to store all files in a single folder with a unique identifier as name. Other features are getting cache memory analytics and model_output usage to delete underused files. 

Notes:
    -Downlading a single model output file takes about 2-3 min with good internet. 
    -Each model output is about ~1.5 gb of data. Be mindful when downloading many model outputs. 
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


    