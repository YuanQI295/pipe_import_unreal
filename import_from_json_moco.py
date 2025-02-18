import unreal
import json

json_file_path = "C:/Users/STATION10/Desktop/shiyuan_replace_inst_set_01/mesh_info_pivot_ok_01.json"
UNREAL_IMPORT_PATH = "/Game/Assets/BG/"

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def access_key_data(json_data, key):
    if key in json_data:
        return json_data[key]
    else:
        print(f"Key '{key}' not found in JSON data.")
        return None

def spawn_actor_from_asset():
    load_json(json_file_path)
    json_data = load_json(json_file_path)

    # for key, value, in json_data.items():

    for key in json_data.keys():
        asset_json_data = access_key_data(json_data, key)
        key_lower = key.lower()
        vertex_num = asset_json_data.get("vertex_num")
        for prop_folder_path in unreal.EditorAssetLibrary.list_assets(UNREAL_IMPORT_PATH, recursive=False,
                                                                      include_folder=True):
            folder_name = prop_folder_path.rsplit("/", 2)[1]
            folder_name_lower = folder_name.lower()

            if unreal.EditorAssetLibrary.does_directory_exist(prop_folder_path):
                # print(key_lower.split("_", 1)[0], folder_name_lower.split("_", 1)[0], " / ", type(vertex_num), type(folder_name_lower.split("_", 1)[1]))
                if key_lower.split("_", 1)[0] == folder_name_lower.split("_", 1)[0] and str(vertex_num) == folder_name_lower.split("_", 1)[1]:


                    meshes_folder = prop_folder_path + "Meshes/"  # Chemin vers le dossier "Meshes" dans chaque dossier de propriété
                    asset_names = unreal.EditorAssetLibrary.list_assets(meshes_folder, recursive=False, include_folder=False)
                    for asset_name in asset_names:
                        asset = unreal.EditorAssetLibrary.load_asset(asset_name)

                        asset_translate_vector = unreal.Vector(asset_json_data.get('location')[0]*1000,
                                                               asset_json_data.get('location')[1]*-1000,
                                                               asset_json_data.get('location')[2]*1000)

                        asset_scale_vector = unreal.Vector(asset_json_data.get('scale')[0],
                                                           asset_json_data.get('scale')[1],
                                                           asset_json_data.get('scale')[2])

                        # asset_rotation = [asset_json_data.get('rotation')[0]-90.0,
                        #                   asset_json_data.get('rotation')[1]*-1,
                        #                   asset_json_data.get('rotation')[2]*-1]
                        rotator = unreal.Rotator(roll=asset_json_data.get('rotation')[0]-90.0, pitch=asset_json_data.get('rotation')[1]*-1, yaw=asset_json_data.get('rotation')[2]*-1)

                        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, asset_translate_vector, rotator)
                        actor.set_actor_scale3d(asset_scale_vector)

                        # print("actor_name", actor, "key", key, "asset_rotation", "X", asset_json_data.get('rotation')[0],"y", asset_json_data.get('rotation')[1],"z", asset_json_data.get('rotation')[2])

spawn_actor_from_asset()
