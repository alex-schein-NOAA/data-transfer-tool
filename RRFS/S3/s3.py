import boto3
from botocore import UNSIGNED
from botocore.client import Config

class s3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',region_name='us-east-1', config=Config(signature_version=UNSIGNED))
    
    #Fetches file from bucket
    def download_file(self, date_time_string, init_hour_string, file_name, download_path):
        try :

            object_name = self.create_object_name(date_time_string, init_hour_string, file_name)
            with open(f"{download_path}/{file_name}", 'wb') as f:
                print("Downloading File")
                self.s3.download_fileobj(self.bucket_name, object_name, f)
            print("File succesfully downloaded")

        except Exception as e:
            raise Exception(f"File download Error: Failed to download file {object_name} from bucket {self.bucket_name}")

    #Helper function
    #Creates object name for file in bucket
    def create_object_name(self, date_time_string, init_hour_string, file_name):
        date_time = date_time_string.split("-")
        date_time = ''.join(map(str, date_time))
        return f"rrfs_a/rrfs_a.{date_time}/{init_hour_string}/control/{file_name}"
    