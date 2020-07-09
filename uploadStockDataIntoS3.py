import boto3
import logging
import os
from alpha_vantage.timeseries import TimeSeries
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print("Done!")
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    for file in os.listdir():
        if '.csv' in file:
            upload_file_bucket = 'googlestockdata'
            upload_file_key = 'data/' + str(file)
            upload_file(file,upload_file_bucket,upload_file_key)

if __name__ == "__main__":
    main()