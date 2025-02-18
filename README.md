# pipe_import_unreal
This repository contains some codes that simplifies the importation from a data base into Unreal, I worked on this project during my internship at Shards Animation. This was for the render of a short animation sequence in Unreal, the scene was huge, required a lot of materials and textures and optimisations.

````
import_mesh_mat.py import_textures.py
````
creating folders and mesh subfolders to import the meshes and textures

````
create_assign_mat
````
this reassembles the materials and creates material instances and assign the instances to meshes using datas

````
instance_from_json.py
````
