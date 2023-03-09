from argparse import ArgumentParser
from os import makedirs, remove
from os.path import isdir, isfile, join as path_join, dirname
from datetime import datetime, timedelta, timezone


import asyncio
import boto3
import gzip
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


class S3LogFetcher:
    '''
    class to download elb logs from S3 bucket
    '''

    def __init__(self, bucket_name: str, prefix: str) -> None:
        self._bucket_name = bucket_name
        self._prefix = prefix

        # create boto3 s3 client
        self.s3_client = boto3.client('s3')

    async def download_log_and_extract(self, s3_file_key: str, local_file_path: str):
        '''
        downloads log files from s3 bucket in gzip format, then stores file after extraction.
        '''
        # download file
        local_file_path_dir = dirname(local_file_path)
        makedirs(local_file_path_dir, exist_ok=True)
        self.s3_client.download_file(
            self._bucket_name, s3_file_key, local_file_path)

        # extract file
        if isfile(local_file_path):
            extracted_file_path = local_file_path.removesuffix('.gz')
            with gzip.open(local_file_path, 'rb') as f_in, open(extracted_file_path, 'wb') as f_out:
                f_out.write(f_in.read())

            # delete .gz file after extraction
            remove(local_file_path)
            logger.info(f'{s3_file_key} file downloaded and extracted at {extracted_file_path}')

            return True
        
        logger.error(f'Failed to download {s3_file_key}')

        return False

    async def s3_fetch_logs(self, store_location: str, start_time: datetime, end_time: datetime):
        '''
        downloads logs from s3 bucket and stores into specified 
        folder for provided time frame.
        '''
        if not isdir(store_location):
            makedirs(store_location)

        # list objects created in the time frame
        response = self.s3_client.list_objects_v2(
            Bucket=self._bucket_name,
            Prefix=self._prefix,
        )

        # get files in provided time window
        tasks = []
        for obj in response['Contents']:
            key = obj['Key']
            modified_time: datetime = obj['LastModified']

            if start_time <= modified_time <= end_time:
                local_file_path = path_join(store_location, key)

                # download only *.log.gz files
                if not local_file_path.endswith('.log.gz'):
                    continue

                # download file
                tasks.append(self.download_log_and_extract(
                    key, local_file_path))

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = ArgumentParser(prog='s3_log')

    parser.add_argument('-b', '--bucket', dest='bucket_name',
                        help='s3 bucket name', required=True, type=str)
    parser.add_argument('-p', '--prefix', dest='prefix',
                        help='s3 bucket directory prefix', required=True, type=str)
    parser.add_argument('-H', '--hour', dest='hours',
                        help='download logs for specified previous hours from current time', required=False, type=int, default=0)
    parser.add_argument('-m', '--minutes', dest='mins',
                        help='download logs for specified previous mins from current time', required=False, type=int, default=0)
    parser.add_argument('-s', '--seconds', dest='secs',
                        help='download logs for specified previous seconds from current time', required=False, type=int, default=0)
    parser.add_argument('-o', '--output', dest='store_location',
                        help='path of directory to store downloaded logs', type=str, default='./logs')

    args = parser.parse_args()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - \
        timedelta(hours=args.hours, minutes=args.mins, seconds=args.secs)

    log_fetcher = S3LogFetcher(
        bucket_name=args.bucket_name,
        prefix=args.prefix,
    )

    results = asyncio.run(
        log_fetcher.s3_fetch_logs(
            store_location=args.store_location,
            start_time=start_time,
            end_time=end_time
        )
    )
