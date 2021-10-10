import boto3
import os
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

user_id = "01284729137"
main_dir = "image_generator/"
bucket = "01whimsy-storeage-space"
# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url=do_endpoint,
                        aws_access_key_id=do_key,
                        aws_secret_access_key=do_secret)
class ImageStorage():

    def __init__(self, client, bucket, user_id, main_dir, project_id):
        self.client = client
        self.bucket = bucket
        self.user_id = user_id
        self.main_dir = main_dir
        self.project_id = project_id
        self.full_path = f"{main_dir}{user_id}/{project_id}/"

    def created_user_dir(self):
        isExist = os.path.exists(self.full_path)

        if not isExist:
            # Create user dir if it does not exist
            os.makedirs(self.full_path)
            print(f"{self.user_id}'s directory was created at {self.full_path}")

    def find_user_dir_by_id(self):
        pass
    
    def list_all_user_projects(self):
        # Get user 
        contents = self.client.list_objects_v2(Bucket=self.bucket, Prefix=self.full_path)
        project = [directory['Key'] for directory in contents['Contents']]
        return project

    def download_user_project(self):
        pass
    def upload_nft_images(self):
        pass

IS = ImageStorage(client, bucket, user_id, main_dir, "project1")
print(IS.list_all_user_projects())