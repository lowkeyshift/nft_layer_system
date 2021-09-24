import random
import json
import ast
import os
from itertools import product
from itertools import combinations
from itertools import permutations
from dotenv import load_dotenv
import threading

load_dotenv()
do_endpoint = os.getenv("do_spaces_endpoint")
do_key = os.getenv("do_spaces_key")
do_secret = os.getenv("do_spaces_secret")
cwd = os.getcwd()

class MetaDataGen():
    """
    metadata generator to calculate and create all possible combinations 
    """
    def __init__(self, user_id, anchors, layer1, layer2, image_array=None):
        self.user_id = user_id
        self.anchors = anchors
        self.layer1 = layer1
        self.layer2 = layer2
        if image_array == None:
            self.image_array = []

    # Returns true if all images are unique
    def all_images_unique(self,image_list):
        seen = list()
        return not any(i in seen or seen.append(i) for i in image_list)

    def write_to_file(self):
        final_images = {"images": []}
        final_images["images"] = self.image_array
        if os.path.isdir("./nft_image_metadata"):
            with open(f"./nft_image_metadata/{self.user_id}_image_list.json", "a") as final:
                json.dump(final_images, final)
                final.close()
        else:
            os.mkdir("./nft_image_metadata")
            self.write_to_file()

    def total_combinations(self):
        # Need to get image directories from digitalocean
        # Calculate permutations from there
        perm = list(product(self.anchors["image_names"],self.layer1["image_names"],self.layer2["image_names"]))
        total_images = len(perm)
        return total_images
    ## Create optional flag in mock data (True||False)
    ## Used to flag is a layer is optional or to allow None
    def imageObjs(self, total_images):
        for i in range(total_images):
            meta = self.create_new_image_data(total_images)
            self.image_array.append(meta)
        return self.image_array

    def tokenId(self):
        # Register tokenId to each entry
        i = 0
        for item in self.image_array:
            item["tokenId"] = i
            i = i + 1

    def create_new_image_data(self,total_images):
        new_image = {}
        while len(self.image_array) <= total_images:
            # For each trait category, select a random trait based on the weightings
            new_image ["backgrounds"] = random.choices(self.anchors["image_names"], self.anchors["weight"])[0]
            new_image ["layer1"] = random.choices(self.layer1["image_names"], self.layer1["weight"])[0]
            new_image ["layer2"] = random.choices(self.layer2["image_names"], self.layer2["weight"])[0]
            if new_image in self.image_array:
                continue
            else:
                return new_image

# # Testing block
# if __name__ == "__main__":
#     with open(f"{cwd}/randomizers/frontend_mock.json", "r") as js:
#         jsonFile = js.read()
#         json_data = json.loads(jsonFile)
#         anchors = json_data["assets"]["anchor"]
#         layer1 = json_data["assets"]["layer1"]
#         layer2 = json_data["assets"]["layer2"]
#         mdg = MetaDataGen("testuser", anchors, layer1, layer2)
#         total_images = mdg.total_combinations()
#         all_images = mdg.imageObjs(total_images)
#         js.close()
#     if mdg.all_images_unique(all_images) == True:
#         mdg.tokenId()
#         mdg.write_to_file()
#         print("Success: All Unique")
#     else:
#         print("Not 100% unqiue")



        