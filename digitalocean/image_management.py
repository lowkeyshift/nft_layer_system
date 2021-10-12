import boto3
import glob, os
import random
import json
from PIL import Image
from dotenv import load_dotenv
from randomizers.data_randomizer import MetaDataGen
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
resource = boto3.resource('s3',
                        region_name='nyc3',
                        endpoint_url=do_endpoint,
                        aws_access_key_id=do_key,
                        aws_secret_access_key=do_secret)
class ImageStorage():

    def __init__(self, client, resource, bucket, user_id, main_dir, project_id):
        self.client = client
        self.resource = resource
        self.bucket = bucket
        self.user_id = user_id
        self.main_dir = main_dir
        self.project_id = project_id
        self.full_path = f"{main_dir}{user_id}/{project_id}/"
        self.user_path = f"{main_dir}{user_id}/"
    
    def list_all_user_projects(self):
        # Get user 
        contents = self.client.list_objects_v2(Bucket=self.bucket, Prefix=self.full_path)
        project = [directory['Key'] for directory in contents['Contents']]
        return project

    def download_user_project(self):
        contents = self.resource.Bucket(self.bucket)
        for obj in contents.objects.filter(Prefix=self.full_path):
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            if not os.path.isdir(obj.key):
                contents.download_file(obj.key, obj.key)

    def upload_nft_images(self):
        pass

IS = ImageStorage(client, resource, bucket, user_id, main_dir, "project1")
IS.download_user_project()
