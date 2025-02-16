import boto3
import zipfile
import os
from io import BytesIO

def unzip_s3_file(bucket_name, zip_file_key, extract_to_prefix):
    s3 = boto3.client('s3')

    # Download the zip file from S3
    zip_obj = s3.get_object(Bucket=bucket_name, Key=zip_file_key)
    buffer = BytesIO(zip_obj['Body'].read())

    # Unzip the file
    with zipfile.ZipFile(buffer, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_name = file_info.filename
            file_data = zip_ref.read(file_name)

            # Upload the extracted file to S3
            s3.put_object(Bucket=bucket_name, Key=os.path.join(extract_to_prefix, file_name), Body=file_data)

if __name__ == "__main__":
    bucket_name = 'your-bucket-name'
    zip_file_key = 'path/to/your/zipfile.zip'
    extract_to_prefix = 'path/to/extracted/files/'

    unzip_s3_file(bucket_name, zip_file_key, extract_to_prefix)
