import json
import math
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
            #print(rotation)
            euler = [math.radians(float(rotation[axis])) for axis in ['z', 'x', 'y']]
            blender_euler = [math.radians(float(rotation[axis])) for axis in ['z', 'x', 'y']]
            print(rotation)
            print(blender_euler)

load_furniture()
