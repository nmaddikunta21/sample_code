import boto3

def copy_s3_files(bucket_name, source_prefix, destination_prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    
    # List all objects in the source prefix
    for page in paginator.paginate(Bucket=bucket_name, Prefix=source_prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                source_key = obj['Key']
                destination_key = source_key.replace(source_prefix, destination_prefix, 1)
                
                # Copy the object
                copy_source = {'Bucket': bucket_name, 'Key': source_key}
                s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=destination_key)
                print(f'Copied {source_key} to {destination_key}')

if __name__ == "__main__":
    bucket_name = 'your-bucket-name'
    source_prefix = 'source-folder/'
    destination_prefix = 'destination-folder/'

    copy_s3_files(bucket_name, source_prefix, destination_prefix)
