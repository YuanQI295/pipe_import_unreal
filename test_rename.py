import os

def rename_files_in_folder(folder_path):
    # Vérifier si folder_path est un dossier existant, sinon ajuster le chemin
    if os.path.isdir(folder_path):
        base_dir = folder_path

    for prop_name in os.listdir(base_dir): # Parcourir tous les fichiers et dossiers dans base_dir
        maps_folder = os.path.join(base_dir, prop_name, "SUBSTANCE")
        system_asset_path = maps_folder
        maps_files = []

        """ Listing resources """
        if os.path.exists(system_asset_path):
            for file in os.listdir(system_asset_path):  # Trouver tex dans le systeme a travers systeme_asset_path
                if file.lower().find(".png") != -1:
                    maps_files.append(file)
                    print(maps_files)

        # print("list_des_maps =", maps_files)
        #
        # for filename in maps_files: # Parcourir tous les fichiers PNG trouvés dans maps_folder
        #     file_path = os.path.join(maps_folder, filename)
        #     file_path = file_path.replace("\\", "/")
        #     print("path =", file_path)
        #
        #     # Split the filename into parts
        #     parts = filename.rsplit('.', 1)
        #     parts0 = parts[0]
        #     parts = parts0.rsplit('_', 2)
        #     print("parts =", parts)
        #
        #     if len(parts) == 3 and 'Normal' or "BaseColor" or "OcclusionRoughnessMetallic" in parts[2]:
        #         # Extract the parts
        #         before_number = parts[0]
        #         number = parts[1]
        #         name_part = parts[2]
        #
        #         # Create the new filename
        #         new_name = f"{before_number}_{name_part}_{number}.png"
        #         new_file_path = os.path.join(folder_path, prop_name, "SUBSTANCE/", "UNREAL/", new_name)
        #
        #         # Rename the file
        #         os.rename(file_path, new_file_path)
        #         print(f"Renamed: {file_path} -> {new_file_path}")
        #     else:
        #         print(f"Filename does not match expected pattern: {filename}")

folder_path = ('P:/Projects/MOCO/Reception/20240718/Set_Global_layout_tk001_high_28.ma/MOCO/01_ASSETS/TEXTURE/SETS')

# Rename files
rename_files_in_folder(folder_path)

print("Renaming completed.")
