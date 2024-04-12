import json
def load_furniture():
    print("test")
    with open("/Users/lukastomasek/Desktop/projects/pc-to-blender-addon/playcanvas-scene.json") as file:
        data = json.load(file)
        items = data["items"]
        for index, item in enumerate(items):
            position = item["position"]
            rotation = item["rotation"]
            product = item["product"]
            title = product["title"]
            print(rotation)
            print(float(rotation["x"]), float(rotation["y"]), float(rotation["z"]))

load_furniture()
