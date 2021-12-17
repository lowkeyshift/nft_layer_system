from PIL import Image
import json
import os

def generate_nfts(nft_data):
    """
    Generates the images
    """
    user = nft_data['general']['user'] # Get the user to find files
    root_path = nft_data["assets"]["rootpath"] # Find the assets rootpath
    data = load_metadata_file(user) # Load the metadata file
    if not os.path.isdir("./nft_images"):
        os.mkdir("./nft_images")
    if not os.path.isdir(f"./nft_images/{user}"):
        os.mkdir(f"./nft_images/{user}")
    for nft in data: # Loop through nfts in the metadata file
        background_data = data[nft]['image'].pop('backgrounds') # Get the background layer
        layer_path = f"{root_path}/{nft_data['assets']['backgrounds']['subdir']}" # Create the path to the backgrounds
        background = Image.open(f"{layer_path}/{background_data}.{nft_data['assets']['backgrounds']['format']}") # Open the background image
        for layer in data[nft]["image"]: # Loop through the rest of the layers
            if data[nft]['image'][layer]:
                layer_path = f"{root_path}/{nft_data['assets'][layer]['subdir']}" # Get path to the layer
                new_layer = Image.open(f"{layer_path}/{data[nft]['image'][layer]}.{nft_data['assets'][layer]['format']}") # Open the image specified in the metadata
                background.paste(new_layer, (0,0), new_layer) # Add it to the background
        background.save(f"./nft_images/{user}/{nft}.png") # Save the image as a png

def create_cardano_metadata(nft_data, list_of_nfts):
    """
    Generates the metadata required in cardano cli.
    """
    user = nft_data['general']['user']
    policy = nft_data["general"]["policyId"]
    data = load_metadata_file(user)
    metadata = {"721": {policy: {}}}
    for nft in list_of_nfts:
        metadata["721"][policy][nft] = data[nft]["metadata"]
    return metadata
    
def load_metadata_file(user):
    """
    Loads the metadata from file made in nft_generator.py
    """
    with open(f"./nft_image_metadata/{user}_image_list.json", "r") as file:
        return (json.load(file))
    
with open(f"randomizers/test.json", "r") as file:
    data = json.load(file)
generate_nfts(data)


with open('test.json','w') as file:
    json.dump(create_cardano_metadata(data, ["TestSeries0", "TestSeries1", "TestSeries2"]), file, indent=4)
