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
    def __init__(self, json_file):
        self.image_array = []
        self.parse_file(json_file) # Parse the json file
        self.layer_names = [layer for layer in self.assets if layer not in ["rootpath", "ending_dimensions"]] # Loop through the assets in the json and store all the layer names (eg layer1, layer2)

    def parse_file(self, json_file):
        """
        Parses the json file passed into the MetaDataGen function and stores the data into variables
        """
        with open(json_file, "r") as file:
            data = json.load(file)
        self.metadata = data["metadata"]
        self.general = data["general"]
        self.assets = data["assets"]
        
    # Returns true if all images are unique
    def all_images_unique(self, image_list):
        """
        Checks to ensure all of the images which have been generated are unique
        """
        seen = list()
        return not any(i in seen or seen.append(i) for i in image_list)

    def write_to_file(self):
        """
        Writes the metadata which has been generated into an output file
        """
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
        """
        Generates the metadata for the project
        """
        final = {}
        name = self.metadata.pop("name") # Retireves the name of the project
        for image in self.image_array: # Loops through the images in the array
            tokenId = str(image.pop("tokenId")) # Gets the token ID of the image
            image_name = name + tokenId # Combines the name of the project with the token ID
            final[image_name] = {"metadata": {}, "image": {}} # Adds empty dictionaries to the final dict
            final[image_name]["metadata"] = {"name": name + f" #{tokenId}"} # Update the metadata section of the metadata
            for entry in self.metadata:
                final[image_name]["metadata"][entry] = self.metadata[entry]
            final[image_name]["metadata"]["tags"] = [tag for tag in image.values() if tag is not None]
            final[image_name]["image"] = image # Add the image details to the metadata
        if not os.path.isdir("./nft_image_metadata"):
            os.mkdir("./nft_image_metadata")
        with open(f"./nft_image_metadata/{self.general['user']}_image_list.json", "w") as file:
            json.dump(final, file, indent = 4)
        
    def total_combinations(self):
        """
        Calculates the total number of combinations
        """
        images = [self.assets[image]["image_names"] for image in self.layer_names]
        perm = list(product(*images))
        total_images = len(perm)
        return total_images
    
    def imageObjs(self):
        """
        Loop through and generate the number of images required
        """
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
        """
        Create a unique image
        """
        new_image = {}
        while len(self.image_array) <= total_images:
            # For each trait category, select a random trait based on the weightings
            for layer in self.layer_names:
                new_image[layer] = random.choices(self.assets[layer]["image_names"], self.assets[layer]["weight"])[0]
            if new_image in self.image_array:
                continue
            else:
                return new_image


mdg = MetaDataGen(f"test.json")
mdg.imageObjs()
mdg.tokenId()
mdg.final_metadata()
 # Testing block

