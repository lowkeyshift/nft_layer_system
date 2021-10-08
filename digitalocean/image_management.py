import boto3
import os
import random
import json
from dotenv import load_dotenv
from botocore.client import Config


# To be determined.
# Testing block
cwd = os.getcwd()
load_dotenv()
do_endpoint = os.getenv("do_spaces_endpoint")
do_full_uri = os.getenv("do_spaces_full_uri")
do_region = os.getenv("do_spaces_region")
do_key = os.getenv("do_spaces_key")
do_secret = os.getenv("do_spaces_secret")

# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url=do_endpoint,
                        aws_access_key_id=do_key,
                        aws_secret_access_key=do_secret)

# List all buckets on your account.
response = client.list_buckets()
spaces = [space['Name'] for space in response['Buckets']]
print("Spaces List: %s" % spaces)

# Get Bucket Contents
contents = client.list_objects_v2(Bucket=spaces[0])
directory = [directory['Key'] for directory in contents['Contents']]
if 'image_generator/' in directory:
    num_dex = directory.index("image_generator/")
    print("Spaces Files: %s" % directory[num_dex])