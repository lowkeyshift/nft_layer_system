import boto3
import os
import shutil
from dotenv import load_dotenv
from botocore.client import Config

# To be determined.
# Testing block
# cwd = os.getcwd()
load_dotenv()
do_endpoint = os.getenv("do_spaces_endpoint")
do_full_uri = os.getenv("do_spaces_full_uri")
do_region = os.getenv("do_spaces_region")
do_key = os.getenv("do_spaces_key")
do_secret = os.getenv("do_spaces_secret")

class ImageStorage():
    """
    ImageStorage is the cloud storage management code
    This code manages the downloading and uploading of assets
    and mirrors the directory structure from the cloud storage
    """

    def __init__(self, user_id, main_dir, project_id):
        self.bucket = os.getenv("do_bucket")
        self.user_id = user_id
        self.main_dir = main_dir
        self.project_id = project_id
        self.full_path = f"{main_dir}{user_id}/{project_id}/"
        self.user_path = f"{main_dir}{user_id}/"

        # Initialize a session using DigitalOcean Spaces.
        session = boto3.session.Session()
        self.client = session.client('s3',
                        region_name=do_region,
                        endpoint_url=do_endpoint,
                        aws_access_key_id=do_key,
                        aws_secret_access_key=do_secret)
        self.resource = boto3.resource('s3',
                        region_name=do_region,
                        endpoint_url=do_endpoint,
                        aws_access_key_id=do_key,
                        aws_secret_access_key=do_secret)
    
    def list_remote_user_projects(self):
        # Get user 
        contents = self.client.list_objects_v2(Bucket=self.bucket, Prefix=self.full_path)
        project = [directory['Key'] for directory in contents['Contents']]
        return project

    def IsObjectExists(self, filename):
        unq_file_path = f"{self.full_path}{filename}"
        print(unq_file_path)
        contents = self.resource.Bucket(self.bucket)
        for object_summary in contents.objects.filter(Prefix=unq_file_path):
            print(object_summary)
            return True
        return False

    def delete_remote_file(self, del_file):
        if(self.IsObjectExists(del_file)):
            self.resource.Object(self.bucket, f"{self.full_path}{del_file}").delete()
            return f"Deleted {del_file}"
        else:
            return f"Directory/File \"{del_file}\" doesn't exists"
    
    def delete_local(self, path, ):
        # checking whether file exists or not
        if os.path.exists(path):
            isFile = os.path.isfile(path)
            isDirectory = os.path.isdir(path)

            if isFile == True:
                # removing the file using the os.remove() method

                os.remove(path)
            if isDirectory == True:
                # checking whether the folder is empty or not
                if len(os.listdir(path)) == 0:
                    # removing the file using the os.remove() method
                    os.rmdir(path)
                else:
                    # TODO: Build to remove single directory or whole project
                    shutil.rmtree(path)
        else:
            # file not found message
            print(f"No file or directory in path: \"{path}\"")

    def download_remote_project(self):
        contents = self.resource.Bucket(self.bucket)
        for obj in contents.objects.filter(Prefix=self.full_path):
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            if not os.path.isdir(obj.key):
                contents.download_file(obj.key, obj.key)
# Test Run
user_id = "01284729137"
main_dir = "image_generator/"
project = "project1"
IS = ImageStorage(user_id, main_dir, project)
# IS.download_user_project()
IS.delete_user_file("anchors/600_600_female.png")
