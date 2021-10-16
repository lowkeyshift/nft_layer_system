# with open(f"{cwd}/randomizers/frontend_mock.json", "r") as js:
#     jsonFile = js.read()
#     json_data = json.loads(jsonFile)
#     anchors = json_data["assets"]["anchor"]
#     layer1 = json_data["assets"]["layer1"]
#     layer2 = json_data["assets"]["layer2"]
#     mdg = MetaDataGen("AppTestUserName", anchors, layer1, layer2)
#     total_images = mdg.total_combinations()
#     all_images = mdg.imageObjs(total_images)
#     js.close()
# if mdg.all_images_unique(all_images) == True:
#     mdg.tokenId()
#     mdg.write_to_file()
#     print("Success: All Unique")
# else:
#     print("Not 100% unqiue")

# with open(f"{cwd}/nft_image_metadata/AppTestUserName", "r") as js:
#     jsonFile = js.read()
#     json_data = json.loads(jsonFile)