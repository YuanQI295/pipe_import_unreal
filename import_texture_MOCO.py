import unreal
import os

PROPS_PATH = 'P:/Projects/MOCO/Reception/20240718/Set_Global_layout_tk001_high_28.ma/MOCO/01_ASSETS/TEXTURE/SETS/'
UNREAL_IMPORT_PATH = "/Game/Assets/TEX/"


def import_maps():
    if os.path.isdir(PROPS_PATH):
        base_dir = PROPS_PATH

    for prop_name in os.listdir(base_dir):

        maps_folder = base_dir + prop_name + "/SUBSTANCE/"
        # unreal.log(maps_folder)


        asset_unreal_folder = UNREAL_IMPORT_PATH + prop_name + "/"
        if not unreal.EditorAssetLibrary.does_directory_exist(asset_unreal_folder):
            unreal.EditorAssetLibrary.make_directory(asset_unreal_folder)

        maps_files = []

        """ Listing resources """
        if os.path.exists(maps_folder):
            for file in os.listdir(maps_folder):  # Trouver tex dans le systeme a travers systeme_asset_path
                if file.lower().find(".exr"):
                    maps_files.append(file)
                    # unreal.log(f"{prop_name} CONTIENT {file}")

        """ Texture """

        for texture_name in maps_files:
            print(texture_name)
            maps_unreal_folder = asset_unreal_folder + "Textures/"  # Definir le dossier unreal où mettre les tex
            if not unreal.EditorAssetLibrary.does_directory_exist(maps_unreal_folder):
                unreal.EditorAssetLibrary.make_directory(maps_unreal_folder)
            #texture_name = texture_name.rsplit(".", 1)[0]
            if texture_name.find("_D_1001") != -1:
                texture_filepath = maps_folder + texture_name
                texture_task = build_import_assets(texture_filepath, maps_unreal_folder, texture_name)

                execute_import_task([texture_task])

                albedo_asset = unreal.EditorAssetLibrary.load_asset(maps_unreal_folder + texture_name.rsplit(".", 1)[0] + "_exr")
                albedo_asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)
                unreal.EditorAssetLibrary.save_loaded_asset(albedo_asset)
                unreal.EditorAssetLibrary.checkout_loaded_asset(albedo_asset)

            if texture_name.find("_AO_1001") != -1 or texture_name.find("_H_1001") != -1 or texture_name.find("_R_1001") != -1 or texture_name.find("_Metal_1001") != -1 or texture_name.find("_Mask_1001") != -1:
                texture_filepath = maps_folder + texture_name
                texture_task = build_import_assets(texture_filepath, maps_unreal_folder, texture_name)

                execute_import_task([texture_task])

                aorm_asset = unreal.EditorAssetLibrary.load_asset(maps_unreal_folder + texture_name.rsplit(".", 1)[0] + "_exr")
                aorm_asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_MASKS)
                unreal.EditorAssetLibrary.save_loaded_asset(aorm_asset)
                unreal.EditorAssetLibrary.checkout_loaded_asset(aorm_asset)

            if texture_name.find("_N_1001") != -1:
                texture_filepath = maps_folder + texture_name
                texture_task = build_import_assets(texture_filepath, maps_unreal_folder, texture_name)

                execute_import_task([texture_task])

                normal_asset = unreal.EditorAssetLibrary.load_asset(maps_unreal_folder + texture_name.rsplit(".", 1)[0] + "_exr")
                normal_asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
                normal_asset.set_editor_property('flip_green_channel', True)
                unreal.EditorAssetLibrary.save_loaded_asset(normal_asset)
                unreal.EditorAssetLibrary.checkout_loaded_asset(normal_asset)



def build_import_assets(filename, destination_path, asset_name, update=True, options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', asset_name)
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', update)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


def execute_import_task(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)


import_maps()
