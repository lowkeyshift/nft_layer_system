import random
import json
import ast
import os


cwd = os.getcwd()
total_images = 30
final_images = {"images": []}
new_image = {}
all_images = []

class Metadata():
    """
    Random image json metadata generator
    """

    def __init__(self, json_data):
        self.json_data = json_data
        # self.new_image = new_image

    # Returns true if all images are unique
    def all_images_unique(self, image_list):
        seen = list()
        return not any(i in seen or seen.append(i) for i in image_list)

    def kickoff(self):
        # count = 0
        for i in range(total_images):
            new_trait_image = self.create_new_image_data()
            all_images.append(new_trait_image)
            # count = count + 1
            # print(count)
        
        final_images["images"] = [all_images]
        with open("randamized_image_list.json", "a") as final:
            json.dump(final_images, final)
        # print(final_images)


    def create_new_image_data(self):
        
        anchors = self.json_data["assets"]["anchor"]
        layer1 = self.json_data["assets"]["layer1"]
        layer2 = self.json_data["assets"]["layer2"]
        # For each trait category, select a random trait based on the weightings
        new_image ["backgrounds"] = random.choices(anchors["image_names"], anchors["weight"])[0]
        new_image ["layer1"] = random.choices(layer1["image_names"], layer1["weight"])[0]
        new_image ["layer2"] = random.choices(layer2["image_names"], layer2["weight"])[0]
        if self.all_images_unique(all_images):
            return new_image


# Testing block
if __name__ == "__main__":
    with open(f"{cwd}/randomizers/frontend_mock.json", "r") as js:
        jsonFile = js.read()
        json_data = json.loads(jsonFile)
        md = Metadata(json_data)
        md.kickoff()