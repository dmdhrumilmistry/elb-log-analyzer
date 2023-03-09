import boto3
from os import makedirs
from os.path import isdir, join as path_join
from datetime import datetime # , timedelta

def s3_fetch_logs(bucket_name:str, prefix:str ,store_location:str, start_time:datetime, end_time:datetime=None):
    '''
    downloads logs from s3 bucket and stores into specified 
    folder for provided time frame.
    '''
    if not isdir(store_location):
        makedirs(store_location)

    if not end_time:
        end_time = datetime.utcnow()

    # create boto3 s3 client
    s3 = boto3.client('s3')

    # list objects created in the time frame
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        StartTime=start_time,
        EndTime=end_time
    )

    # download files
    for obj in response['Contents']:
        key = obj['Key']
        local_file_path = path_join(store_location, key)
        s3.download_file(bucket_name, key, local_file_path)