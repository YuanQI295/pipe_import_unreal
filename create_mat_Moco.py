import unreal
import os

# chemin d'import des assets
UNREAL_IMPORT_MAT_PATH = "/Game/Assets/MAT/"
UNREAL_IMPORT_TEXT_PATH = "/Game/Assets/TEX/"
MASTER_MAT_PATH = "/Game/Resources/Shaders/Masters"

def creat_assign_materials():

    slot_names = []

    # Parcours des dossiers dans UNREAL_IMPORT_PATH
    for prop_folder_path in unreal.EditorAssetLibrary.list_assets(UNREAL_IMPORT_TEXT_PATH, recursive=False, include_folder=True):
        print(prop_folder_path)
        if unreal.EditorAssetLibrary.does_directory_exist(prop_folder_path):
            textures_folder = prop_folder_path + "Textures/"  # Chemin vers le dossier "Meshes" dans chaque dossier de propriété
            textures_assets = unreal.EditorAssetLibrary.list_assets(textures_folder, recursive=False, include_folder=False)
            if textures_assets:
                materials_unreal_folder = UNREAL_IMPORT_MAT_PATH + prop_folder_path.rsplit("/", 2)[1]  # Création du dossier "Materials" s'il n'existe pas
                if not unreal.EditorAssetLibrary.does_directory_exist(materials_unreal_folder):
                    unreal.EditorAssetLibrary.make_directory(materials_unreal_folder)

                new_material_name = "/" + prop_folder_path.rsplit("/", 2)[1] + "_Mat_inst"

                new_instance_material_path = materials_unreal_folder + new_material_name
                unreal.log(new_instance_material_path)

                instance_material_asset = unreal.load_asset(MASTER_MAT_PATH + "/IM_Standard")
                new_instance_material = unreal.EditorAssetLibrary.duplicate_loaded_asset(instance_material_asset, new_instance_material_path)

                for texture in textures_assets:  # Attribution des textures aux paramètres du matériel instance
                    texture_asset = unreal.load_asset(texture)

                    if "_D" in texture:
                        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                            new_instance_material, "Map - Diffuse", texture_asset)
                    elif "_R" in texture:
                        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                            new_instance_material, "Map - Roughness", texture_asset)
                    elif "_N" in texture:
                        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                            new_instance_material, "Map - Normal", texture_asset)
                    elif "_Metal" in texture:
                        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                            new_instance_material, "Map - Metallic", texture_asset)


creat_assign_materials()
