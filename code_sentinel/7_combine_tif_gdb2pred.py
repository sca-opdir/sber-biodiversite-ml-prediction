import os
import arcpy
import numpy as np
from datetime import datetime
import re

start_time = datetime.now()

# Chemins d'entrée
input_folder = '6_intersect_tif_cleanage_all'
output_folder = "7_merge_intersect_tif2pred_numpyclean_all"
prefix_groups = ["Pâturage", "Prairie"]
prefix = "Pâturage"
for prefix in prefix_groups:

    print("Start " + prefix)

    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
                 re.search(rf"{prefix}.+\.tif$", f)]
    assert len(tif_files) == 1

    # Chemin vers la geodatabase de sortie
    output_gdb = os.path.join(output_folder, f"{prefix}_output_combined.gdb")
    output_feature_class = os.path.join(output_gdb, "combined_pixels")

    # Vérifier ou créer la geodatabase de sortie
    if not os.path.exists(os.path.dirname(output_gdb)):
        os.makedirs(os.path.dirname(output_gdb))
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), os.path.basename(output_gdb))

    # Obtenir la référence spatiale depuis le premier raster
    raster = arcpy.Raster(tif_files[0])
    spatial_ref = arcpy.Describe(tif_files[0]).spatialReference

    # Créer une feature class vide pour stocker les polygones combinés
    arcpy.CreateFeatureclass_management(
        out_path=output_gdb,
        out_name=os.path.basename(output_feature_class),
        geometry_type="POLYGON",
        spatial_reference=spatial_ref
    )

    # Ajouter les champs pour les 4 bandes
    band_names = [f"Band_{i + 1}" for i in range(4)]
    for band in band_names:
        arcpy.AddField_management(output_feature_class, band, "FLOAT")

    # Convertir le raster en numpy array avec toutes les bandes
    raster_array = arcpy.RasterToNumPyArray(raster, nodata_to_value=-9999)  # (4, rows, cols)
    nodata_value = -9999  # Assigner une valeur pour NoData

    # Obtenir les coordonnées des coins des pixels
    x_min, y_min = raster.extent.XMin, raster.extent.YMin
    x_max, y_max = raster.extent.XMax, raster.extent.YMax
    cell_size = raster.meanCellWidth

    # Initialiser le curseur d'insertion
    with arcpy.da.InsertCursor(output_feature_class, ["SHAPE@"] + band_names) as cursor:
        rows, cols = raster_array.shape[1], raster_array.shape[2]

        # Parcourir chaque pixel
        for row in range(rows):
            for col in range(cols):
                # Extraire les valeurs des 4 bandes
                band_values = raster_array[:, row, col]  # (4,)

                # Vérifier si toutes les valeurs sont NoData, si oui, ignorer le pixel
                if np.all(band_values == nodata_value):
                    continue

                # Définir les coordonnées du polygone (pixel)
                x1 = x_min + col * cell_size
                y1 = y_max - row * cell_size
                x2 = x1 + cell_size
                y2 = y1 - cell_size

                # Créer un polygone carré pour représenter le pixel
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

                # Insérer le polygone et ses valeurs de bandes
                cursor.insertRow([polygon] + band_values.tolist())

print(f"Feature class combinée créée : {output_feature_class}")

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {end_time - start_time}")






