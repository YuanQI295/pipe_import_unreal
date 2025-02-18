import unreal

# Constants
UNREAL_IMPORT_PATH = "/Game/Assets/Props/"
INSTANCE_MATERIAL_FOLDER = "/Game/Materials/"
INSTANCE_MATERIAL_NAME = "M_inst"


def create_and_assign_materials():
    slot_names = []  # Utilisation d'une liste au lieu d'un set

    for prop_folder_path in unreal.EditorAssetLibrary.list_assets(UNREAL_IMPORT_PATH, recursive=False, include_folder=True):
        if not unreal.EditorAssetLibrary.does_directory_exist(prop_folder_path):
            continue

        meshes_folder = f"{prop_folder_path}Meshes/"
        asset_names = unreal.EditorAssetLibrary.list_assets(meshes_folder, recursive=False, include_folder=False)

        for asset_name in asset_names:
            obj = unreal.EditorAssetLibrary.load_asset(asset_name)
            if not isinstance(obj, unreal.StaticMesh):
                continue  # Ignorer les assets qui ne sont pas des StaticMesh

            for slot in obj.static_materials:
                slot_name = str(slot.material_slot_name)

                # Vérifier manuellement si le slot_name existe déjà dans la liste
                if slot_name not in slot_names:
                    slot_names.append(slot_name)

                    materials_folder = f"{prop_folder_path}Materials/"
                    textures_folder = f"{prop_folder_path}Textures/"

                    # Créer le dossier Materials si nécessaire
                    if not unreal.EditorAssetLibrary.does_directory_exist(materials_folder):
                        unreal.EditorAssetLibrary.make_directory(materials_folder)

                    # Charger le material instance de base
                    instance_material_asset = unreal.load_asset(f"{INSTANCE_MATERIAL_FOLDER}{INSTANCE_MATERIAL_NAME}")
                    if not instance_material_asset:
                        unreal.log_error(f"Material instance template '{INSTANCE_MATERIAL_NAME}' not found in {INSTANCE_MATERIAL_FOLDER}")
                        continue

                    # Créer un nouveau material instance
                    new_material_name = f"{prop_folder_path.rsplit('/', 2)[1]}_{slot_name}"
                    new_material_path = f"{materials_folder}{new_material_name}"
                    new_instance_material = unreal.EditorAssetLibrary.duplicate_loaded_asset(
                        instance_material_asset, new_material_path
                    )

                    # Attribuer les textures au material instance
                    assign_textures_to_material(new_instance_material, textures_folder)

                    # Assigner le nouveau material instance au StaticMesh
                    obj.set_material(0, new_instance_material)
                    unreal.log(f"Assigned new material instance: {new_material_name} to mesh: {obj.get_name()}")

                else:
                    # Si le slot existe déjà, réutiliser le material existant
                    assign_existing_material_to_slot(obj, slot_name, prop_folder_path)


def assign_textures_to_material(material_instance, textures_folder):
    """Assigner les textures au material instance selon les conventions de nommage."""
    texture_assets = unreal.EditorAssetLibrary.list_assets(textures_folder, recursive=False, include_folder=False)
    
    for texture_path in texture_assets:
        texture_asset = unreal.load_asset(texture_path)
        if not texture_asset:
            continue

        if "BaseColor" in texture_path:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                material_instance, "Diffuse", texture_asset
            )
        elif "OcclusionRoughnessMetallic" in texture_path:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                material_instance, "ORM", texture_asset
            )
        elif "Normal" in texture_path:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                material_instance, "Normal", texture_asset
            )


def assign_existing_material_to_slot(mesh, slot_name, prop_folder_path):
    """Réassigner un material existant au StaticMesh si disponible."""
    materials_folder = f"{prop_folder_path}Materials/"
    material_assets = unreal.EditorAssetLibrary.list_assets(materials_folder, recursive=False, include_folder=False)

    for material_path in material_assets:
        if material_path.endswith(slot_name):
            existing_material = unreal.EditorAssetLibrary.load_asset(material_path)
            if existing_material:
                mesh.set_material(0, existing_material)
                unreal.log(f"Reused existing material '{existing_material.get_name()}' for slot '{slot_name}'.")


# Exécuter le script
create_and_assign_materials()
