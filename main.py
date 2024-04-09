import bpy
import json
import urllib.request
import os
import time
from pathlib import Path

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
render_progress = 0

def render_with_cycles(scene):
  bpy.context.scene.render.engine = "CYCLES"
  output_path = str(Path.home() /  "Downloads")
  bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

def load_glb_from_url(url=LOCAL_MODEL_URL, is_local_path=False):
  if is_local_path:
     bpy.ops.import_scene.gltf(filepath=url)
  else:
    filepath = bpy.path.abspath("/Users/lukastomasek/Downloads/temp.glb")
    urllib.request.urlretrieve(url, filepath)
    bpy.ops.import_scene.gltf(filepath=filepath, filter_glob='*.glb', import_pack_images=True)
    os.remove(local_path)

# CREATE UI PANEL CLASS 
class PcToBlenderPanel(bpy.types.Panel):
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

    layout.progress(factor=0.1)


bpy.types.Scene.json_file_path = bpy.props.StringProperty(
  name="JSON File Path",
  subtype="FILE_PATH",
)

# Utils class to load JSON
class LoadJSON(bpy.types.Operator):
  bl_idname = JSON_ID_NAME
  bl_label = "Load JSON"

  def execute(self, context):
    scene = context.scene
    file_path = scene.json_file_path

    if file_path:
     with open(file_path) as file:
        data = json.load(file)
        floor_plan_url = data["floor_plan"]
        load_glb_from_url(floor_plan_url, is_local_path=False)

    else:
      self.report({'WARNING'}, "No JSON file selected")

    return {'FINISHED'}


class RenderScene(bpy.types.Operator):
  bl_idname = "custom.render"
  bl_label = "Render Scene"

  def execute(self, context):
    render_with_cycles(context.scene)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(PcToBlenderPanel)
  bpy.utils.register_class(LoadJSON)
  bpy.utils.register_class(RenderScene)


def unregister():
  bpy.utils.unregister_class(PcToBlenderPanel)
  bpy.utils.unregister_class(LoadJSON)
  bpy.utils.unregister_class(RenderScene)


if __name__ == "__main__":
  register()