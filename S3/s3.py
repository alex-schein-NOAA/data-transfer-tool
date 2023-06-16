import boto3
from botocore import UNSIGNED
from botocore.client import Config

class s3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',region_name='us-east-1', config=Config(signature_version=UNSIGNED))

    
    #Fetches file from bucket
    def download_file(self, object_name, download_path, cfile_name):
        try :
            # object_name = self.create_object_name(date_time_str, init_hour_str, file_name)
            with open(f"{download_path}/{cfile_name}", 'wb') as f:
                print("Downloading File")
                self.s3.download_fileobj(self.bucket_name, object_name, f)
            print("File succesfully downloaded")

        except Exception as e:
            raise Exception(f"File download Error: Failed to download file {object_name} from bucket {self.bucket_name}")

    #Fetches file names in bucket
    def get_files_in_bucket(self, directory=''):
        try :
            s = self.s3.list_objects(Bucket=self.bucket_name, Prefix=directory)
            return s['Contents']
        except :
            raise Exception(f"Bucket connection error: Failed to list files from bucket {self.bucket_name}") 
    