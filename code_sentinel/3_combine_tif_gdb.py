import os
import arcpy
import numpy as np
from datetime import datetime
import re

start_time = datetime.now()

# Chemins d'entrée
input_folder = '2_intersect_tif_cleangdbcorr_all'
output_folder = "3_merge_intersect_tif_numpycleancorr_all_3bands"
prefix_groups = ["Pâturage_Moins", "Pâturage_Plus", "Prairie_Moins", "Prairie_Plus"]

keep_patt = re.compile(r".+2024-08-06.+bands-10m")

# prefix = "Pâturage_Moins"
for prefix in prefix_groups:

    print("Start " + prefix)

    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
                 re.search(rf"{prefix}.+\.tif$", f)]

    tif_files = [x for x in tif_files if keep_patt.match(os.path.basename(x))]
    assert len(tif_files) == 1  # Vérification qu'un seul raster correspond

    # Chemin vers la geodatabase de sortie
    output_gdb = os.path.join(output_folder, f"{prefix}_output_combined.gdb")
    output_feature_class = os.path.join(output_gdb, "combined_pixels")

    # Vérifier ou créer la geodatabase de sortie
    if not os.path.exists(os.path.dirname(output_gdb)):
        os.makedirs(os.path.dirname(output_gdb))
    if not arcpy.Exists(output_gdb):
        arcpy.management.CreateFileGDB(os.path.dirname(output_gdb), os.path.basename(output_gdb))

    # Obtenir la référence spatiale depuis le premier raster
    spatial_ref = arcpy.Describe(tif_files[0]).spatialReference

    # Lire le raster et gérer plusieurs bandes
    raster = arcpy.Raster(tif_files[0])
    raster_array = arcpy.RasterToNumPyArray(raster, nodata_to_value=-9999)  # Remplace nodata

    # Réorganiser les axes si nécessaire (mettre les bandes en dernière position)
    if raster_array.shape[0] == 4:  # Vérifie si la première dimension correspond aux bandes
        raster_array = np.moveaxis(raster_array, 0, -1)  # Passe de (bands, rows, cols) à (rows, cols, bands)

    ## supprimer la 4ème bande

    if raster_array.shape[-1] == 4:  # Si les bandes sont en dernier axe
        raster_array = raster_array[:, :, :3]  # Garde seulement les 3 premières bandes
    else:
        print("ERROR")
        continue
    # Détecter si le raster contient plusieurs bandes
    if len(raster_array.shape) == 3:
        rows, cols, num_bands = raster_array.shape  # Multi-bandes
    else:
        rows, cols = raster_array.shape  # Une seule bande
        num_bands = 1

    print(f"Raster contient {num_bands} bandes")

    # Créer la feature class si elle n'existe pas
    if not arcpy.Exists(output_feature_class):
        arcpy.CreateFeatureclass_management(
            out_path=output_gdb,
            out_name=os.path.basename(output_feature_class),
            geometry_type="POLYGON",
            spatial_reference=spatial_ref
        )

    # Ajouter des champs pour chaque bande du raster
    field_names = [f"Value_Band_{i+1}" for i in range(num_bands)]
    for field_name in field_names:
        arcpy.AddField_management(output_feature_class, field_name, "FLOAT")

    # Dictionnaire pour stocker les valeurs par polygone (clé = WKT du polygone, valeurs = liste des valeurs raster)
    polygon_data = {}

    # Obtenir les coordonnées des coins des pixels
    x_min, y_min = raster.extent.XMin, raster.extent.YMin
    x_max, y_max = raster.extent.XMax, raster.extent.YMax
    cell_size = raster.meanCellWidth

    # Parcourir les pixels et les associer à des polygones
    for row in range(rows):
        for col in range(cols):
            # Extraire les valeurs de chaque bande
            if num_bands > 1:
                values = raster_array[row, col, :].tolist()  # Liste des valeurs par bande
            else:
                values = [raster_array[row, col]]  # Une seule valeur

            if all(v == -9999 for v in values):  # Ignorer les pixels nodata
                continue

            x1 = x_min + col * cell_size
            y1 = y_max - row * cell_size
            x2 = x1 + cell_size
            y2 = y1 - cell_size

            # Définir le polygone comme un carré
            polygon = arcpy.Polygon(
                arcpy.Array([
                    arcpy.Point(x1, y1),
                    arcpy.Point(x2, y1),
                    arcpy.Point(x2, y2),
                    arcpy.Point(x1, y2),
                    arcpy.Point(x1, y1)
                ]),
                spatial_ref
            )
            polygon_wkt = polygon.WKT

            # Ajouter les valeurs au dictionnaire
            polygon_data[polygon_wkt] = values

    # Insérer les polygones et les valeurs agrégées dans la feature class
    with arcpy.da.InsertCursor(output_feature_class, ["SHAPE@"] + field_names) as cursor:
        for polygon_wkt, values in polygon_data.items():
            polygon = arcpy.FromWKT(polygon_wkt)
            cursor.insertRow([polygon] + values)

    print(f"Feature class combinée créée : {output_feature_class}")

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {end_time - start_time}")
