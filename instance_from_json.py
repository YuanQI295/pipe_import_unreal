import unreal
import json

# Constants
JSON_FILE_PATH = "C:/Users/STATION10/Desktop/shiyuan_replace_inst_set_01/mesh_info_pivot_ok_01.json"
UNREAL_IMPORT_PATH = "/Game/Assets/BG/"

def load_json(file_path):
    """Charge et retourne les données JSON depuis le fichier spécifié."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        unreal.log_error(f"Fichier JSON introuvable : {file_path}")
        return None
    except json.JSONDecodeError:
        unreal.log_error(f"Erreur lors du décodage du fichier JSON : {file_path}")
        return None

def get_asset_json_data(json_data, key):
    """Retourne les données de l'asset depuis le JSON pour une clé donnée."""
    return json_data.get(key, None)

def get_matching_folder(json_key, vertex_num):
    """Recherche un dossier Unreal correspondant au nom et au nombre de sommets."""
    for folder_path in unreal.EditorAssetLibrary.list_assets(UNREAL_IMPORT_PATH, recursive=False, include_folder=True):
        folder_name = folder_path.rsplit("/", 2)[1].lower()

        if not unreal.EditorAssetLibrary.does_directory_exist(folder_path):
            continue

        json_key_lower = json_key.lower().split("_", 1)[0]
        folder_name_lower = folder_name.split("_", 1)[0]
        folder_vertex_num = folder_name.split("_", 1)[1] if "_" in folder_name else None

        if json_key_lower == folder_name_lower and str(vertex_num) == folder_vertex_num:
            return folder_path
    return None

def spawn_actor(asset, asset_data):
    """Crée et place un acteur Unreal dans la scène avec les transformations spécifiées."""
    location = unreal.Vector(
        asset_data['location'][0] * 1000,
        asset_data['location'][1] * -1000,
        asset_data['location'][2] * 1000
    )
    scale = unreal.Vector(*asset_data['scale'])
    rotation = unreal.Rotator(
        roll=asset_data['rotation'][0] - 90.0,
        pitch=asset_data['rotation'][1] * -1,
        yaw=asset_data['rotation'][2] * -1
    )

    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, location, rotation)
    actor.set_actor_scale3d(scale)
    unreal.log(f"Acteur créé : {actor.get_name()} avec échelle {scale} et rotation {rotation}")

def process_assets(json_data):
    """Traite chaque entrée du JSON et tente de créer les acteurs Unreal correspondants."""
    for key in json_data:
        asset_data = get_asset_json_data(json_data, key)
        if not asset_data:
            unreal.log_warning(f"Aucune donnée pour la clé : {key}")
            continue

        folder_path = get_matching_folder(key, asset_data.get("vertex_num"))
        if not folder_path:
            unreal.log_warning(f"Aucun dossier trouvé pour {key} avec vertex_num {asset_data.get('vertex_num')}")
            continue

        meshes_folder = f"{folder_path}Meshes/"
        asset_names = unreal.EditorAssetLibrary.list_assets(meshes_folder, recursive=False, include_folder=False)

        for asset_name in asset_names:
            asset = unreal.EditorAssetLibrary.load_asset(asset_name)
            if asset:
                spawn_actor(asset, asset_data)
            else:
                unreal.log_warning(f"Impossible de charger l'asset : {asset_name}")

def main():
    """Point d'entrée principal du script."""
    json_data = load_json(JSON_FILE_PATH)
    if json_data:
        process_assets(json_data)

# Lancer le script
main()
