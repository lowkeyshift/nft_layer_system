import random
import json
import ast
import os
from itertools import product
from itertools import combinations
from itertools import permutations
#from dotenv import load_dotenv
import threading

#load_dotenv()
do_endpoint = os.getenv("do_spaces_endpoint")
do_key = os.getenv("do_spaces_key")
do_secret = os.getenv("do_spaces_secret")
cwd = os.getcwd()

class MetaDataGen():
    """
    metadata generator to calculate and create all possible combinations 
    """
    #def __init__(self, user_id, anchors, layer1, layer2, metadata, image_array=None):
    def __init__(self, json_file):
        self.image_array = []
        self.parse_file(json_file)
        self.layer_names = [layer for layer in self.assets if layer not in ["rootpath", "ending_dimensions"]]
        #self.user_id = user_id
        #self.anchors = anchors
        #self.layer1 = layer1
        #self.layer2 = layer2
        #self.metadata = metadata
        #if image_array == None:
        #    self.image_array = []

    def parse_file(self, json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
        self.metadata = data["metadata"]
        self.general = data["general"]
        self.assets = data["assets"]
        
    # Returns true if all images are unique
    def all_images_unique(self, image_list):
        seen = list()
        return not any(i in seen or seen.append(i) for i in image_list)

    def write_to_file(self):
        final_images = {"images": []}
        final_images["images"] = self.image_array
        if os.path.isdir("./nft_image_metadata"):
            with open(f"./nft_image_metadata/{self.user_id}_image_list.json", "w") as final:
                json.dump(final_images, final, indent = 4)
                final.close()
        else:
            os.mkdir("./nft_image_metadata")
            self.write_to_file()

    def final_metadata(self):
        final = {}
        name = self.metadata.pop("name")
        for image in self.image_array:
            tokenId = str(image.pop("tokenId"))
            image_name = name + tokenId
            final[image_name] = {"metadata": {}, "image": {}}
            final[image_name]["metadata"] = {"name": name + f" #{tokenId}"}
            for entry in self.metadata:
                final[image_name]["metadata"][entry] = self.metadata[entry]
            final[image_name]["metadata"]["tags"] = [tag for tag in image.values() if tag is not None]
            final[image_name]["image"] = image
        if not os.path.isdir("./nft_image_metadata"):
            os.mkdir("./nft_image_metadata")
        with open(f"./nft_image_metadata/{self.general['user']}_image_list.json", "w") as file:
            json.dump(final, file, indent = 4)
        
    def total_combinations(self):
        # Need to get image directories from digitalocean
        # Calculate permutations from there
        images = [self.assets[image]["image_names"] for image in self.layer_names]
        perm = list(product(*images))
        total_images = len(perm)
        return total_images
    ## Create optional flag in mock data (True||False)
    ## Used to flag is a layer is optional or to allow None
    
    def imageObjs(self):
        for i in range(self.general["amount"]):
            meta = self.create_new_image_data(self.general["amount"])
            self.image_array.append(meta)
        return self.image_array

    def tokenId(self):
        # Register tokenId to each entry
        i = 0
        for item in self.image_array:
            item["tokenId"] = i
            i = i + 1

    def create_new_image_data(self, total_images):
        new_image = {}
        while len(self.image_array) <= total_images:
            # For each trait category, select a random trait based on the weightings
            for layer in self.layer_names:
                new_image[layer] = random.choices(self.assets[layer]["image_names"], self.assets[layer]["weight"])[0]
            if new_image in self.image_array:
                continue
            else:
                return new_image


mdg = MetaDataGen(f"randomizers/test.json")
total_images = mdg.total_combinations()
print(total_images)
mdg.imageObjs()
#print(mdg.image_array)
mdg.tokenId()
#print(mdg.image_array)
mdg.final_metadata()
 # Testing block

