import unreal
import os

PROPS_PATH = "C:/Users/STATION10/Desktop/shiyuan_replace_inst_set_01/export_fbx_separer/"
UNREAL_IMPORT_PATH = "/Game/Assets/BG/"


def import_meshes(path):
    for prop_name in os.listdir(path):
        fbx_folder = path
        object_name = prop_name.split("_", 1)[0] + "_" + prop_name.rsplit("_", 1)[1]
        object_name = object_name.split(".", 1)[0]
        asset_unreal_folder = UNREAL_IMPORT_PATH + object_name + "/"
        # unreal.log(asset_unreal_folder)
        if not unreal.EditorAssetLibrary.does_directory_exist(asset_unreal_folder):
            unreal.EditorAssetLibrary.make_directory(asset_unreal_folder)

        mesh_files = []


        """ Listing resources """
        if os.path.isdir(fbx_folder):  # Vérifiez si c'est bien un dossier
            for file in os.listdir(fbx_folder):

                if file.lower().endswith(".fbx"):  # Utilisez endswith pour vérifier l'extension
                    mesh_files.append(file)
        else:
            unreal.log_warning(f"Directory not found: {fbx_folder}")

        unreal.log(mesh_files)

        """ Meshes """
        for mesh in mesh_files:
            asset_name = mesh.replace(".fbx", "").replace(" ", "_")
            mesh_unreal_folder = asset_unreal_folder + "Meshes/"
            object_name_lower = object_name.lower()
            mesh_lower = mesh.lower().rsplit(".", 1)[0]
            if not unreal.EditorAssetLibrary.does_directory_exist(mesh_unreal_folder):
                unreal.EditorAssetLibrary.make_directory(mesh_unreal_folder)

            unreal.log(object_name_lower)
            unreal.log(mesh_lower)

            if mesh_lower.startswith(object_name_lower.split("_", 1)[0]) and mesh_lower.endswith(object_name_lower.rsplit("_", 1)[1]):

                mesh_options = unreal.FbxImportUI()

                mesh_options.set_editor_property('import_mesh', True)
                mesh_options.set_editor_property('import_materials', False)
                mesh_options.set_editor_property('import_textures', False)
                mesh_options.set_editor_property('import_as_skeletal', False)
                mesh_options.set_editor_property('reset_to_fbx_on_material_conflict', False)
                mesh_options.set_editor_property('override_full_name', True)

                mesh_options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
                mesh_options.static_mesh_import_data.set_editor_property('import_uniform_scale', 10.0)
                mesh_options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
                mesh_options.static_mesh_import_data.set_editor_property('combine_meshes', False)
                mesh_options.static_mesh_import_data.set_editor_property('build_nanite', True)
                mesh_options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
                mesh_options.texture_import_data.set_editor_property('material_search_location', unreal.MaterialSearchLocation.DO_NOT_SEARCH)
                mesh_options.static_mesh_import_data.set_editor_property('convert_scene', True)
                mesh_options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', False)
                mesh_options.static_mesh_import_data.set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)

                fbx_task = unreal.AssetImportTask()
                fbx_task.set_editor_property('automated', True)
                fbx_task.set_editor_property('destination_name', asset_name)
                fbx_task.set_editor_property('destination_path', mesh_unreal_folder)
                fbx_task.set_editor_property('filename', fbx_folder + mesh)
                fbx_task.set_editor_property('replace_existing', True)
                fbx_task.set_editor_property('save', True)
                fbx_task.set_editor_property('options', mesh_options)

                unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([fbx_task])


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


import_meshes(PROPS_PATH)
