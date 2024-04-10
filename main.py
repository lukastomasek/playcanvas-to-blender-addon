import bpy
import json
import urllib.request
import os
import time
from pathlib import Path

# Addon Info
bl_info = {
  "name": "Playcanvas Scene Convertor",
  "description": "Playcanvas to Blender Addon for recreating scenes and high quality rendering",
  "author": "Lukas Tomasek",
  "version": (0, 1),
  "blender": (4, 0, 0),
  "location": "View3D > Side bar > Tool",
  "category": "Scene"
}


LOCAL_MODEL_URL = ""
JSON_ID_NAME = "custom.load_json"


#####
# UTILITY CLASSES
####

class RenderEngine():
  def render(self):
    bpy.context.scene.render.engine = "CYCLES"
    output_path = str(Path.home() /  "Downloads")
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)


class Loader():
  def load_glb_from_url(self, url=LOCAL_MODEL_URL, is_local_path=False):
    if is_local_path:
       bpy.ops.import_scene.gltf(filepath=url)
    else:
      local_path = str(Path.home() /  "Downloads/temp.glb")
      filepath = bpy.path.abspath(local_path)
      urllib.request.urlretrieve(url, filepath)
      bpy.ops.import_scene.gltf(filepath=filepath, filter_glob='*.glb', import_pack_images=True)
      os.remove(local_path)

#####
# INTERFACE
####

class Panel(bpy.types.Panel):
  bl_label = "Playcanvas Scene Convertor"
  bl_idname = "pc_to_blender"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_category = "Tool"

  def draw(self, context):
    layout = self.layout
    scene = context.scene

    layout.prop(scene, "json_file_path", text="JSON File")
    layout.operator(JSON_ID_NAME, text="Load JSON")

    layout.label(text="Rendering")
    layout.operator("custom.render", text="Render Scene")


#####
# INTERFACE OPERATORS/CALLBACKS
####

bpy.types.Scene.json_file_path = bpy.props.StringProperty(
  name="JSON File Path",
  subtype="FILE_PATH",
)

class LoadJSON(bpy.types.Operator):
  bl_idname = JSON_ID_NAME
  bl_label = "Load JSON"
  loader = Loader()

  def execute(self, context):
    scene = context.scene
    file_path = scene.json_file_path

    if file_path:
     with open(file_path) as file:
        data = json.load(file)
        floor_plan_url = data["floor_plan"]
        self.loader.load_glb_from_url(floor_plan_url, is_local_path=False)
    else:
      self.report({'WARNING'}, "No JSON file selected")

    return {'FINISHED'}

class RenderScene(bpy.types.Operator):
  bl_idname = "custom.render"
  bl_label = "Render Scene"
  render_engine = RenderEngine()

  def execute(self, context):
    self.render_engine.render()
    return {'FINISHED'}

def register():
  bpy.utils.register_class(Panel)
  bpy.utils.register_class(LoadJSON)
  bpy.utils.register_class(RenderScene)


def unregister():
  bpy.utils.unregister_class(Panel)
  bpy.utils.unregister_class(LoadJSON)
  bpy.utils.unregister_class(RenderScene)


if __name__ == "__main__":
  register()