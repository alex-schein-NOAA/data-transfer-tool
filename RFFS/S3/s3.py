import boto3

class s3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',region_name='us-east-1')
    
    #Fetches file from bucket
    def fetch_file(self, date_time_string, init_hour_string, file_name):
        try :

            object_name = self.create_object_name(date_time_string, init_hour_string, file_name)
            with open(file_name, 'wb') as f:
                self.s3.download_fileobj(self.bucket_name, object_name,f)
               
        except :
            raise Exception(f"File download Error: Failed to download file {object_name} from bucket {self.bucket_name}")

    #Helper function
    #Creates object name for file in bucket
    def create_object_name(self, date_time_string, init_hour_string, file_name):
        return f"rrfs_a/rrfs_a.{date_time_string}/{init_hour_string}/control/{file_name}"
    