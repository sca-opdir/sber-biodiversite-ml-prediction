import os
import arcpy
import numpy as np
from datetime import datetime
import re

start_time = datetime.now()

# Chemins d'entrée
input_folder = '2_intersect_tif_cleangdbcorr_all'
output_folder = "3_merge_intersect_tif_numpycleancorr_all"
prefix_groups = ["Pâturage_Moins", "Pâturage_Plus", "Prairie_Moins", "Prairie_Plus"]
# prefix_groups = ["Pâturage_Moins"]
for prefix in prefix_groups:

    print("Start " + prefix)

    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
                 re.search(rf"{prefix}.+\.tif$", f)]

    # Chemin vers la geodatabase de sortie
    output_gdb = os.path.join(output_folder, f"{prefix}_output_combined.gdb")
    output_feature_class = os.path.join(output_gdb, "combined_pixels")

    # Vérifier ou créer la geodatabase de sortie
    if not os.path.exists(os.path.dirname(output_gdb)):
        os.makedirs(os.path.dirname(output_gdb))
    if not arcpy.Exists(output_gdb):
        arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), os.path.basename(output_gdb))

    # Obtenir la référence spatiale depuis le premier raster
    spatial_ref = arcpy.Describe(tif_files[0]).spatialReference

    # Créer une feature class vide pour stocker les polygones combinés
    arcpy.CreateFeatureclass_management(
        out_path=output_gdb,
        out_name=os.path.basename(output_feature_class),
        geometry_type="POLYGON",
        spatial_reference=spatial_ref
    )

    # Ajouter les champs nécessaires pour les rasters
    field_names = ["Value_" + os.path.basename(tif).split('.')[0] for tif in tif_files]
    for field_name in field_names:
        arcpy.AddField_management(output_feature_class, field_name, "FLOAT")

    # Dictionnaire pour stocker les valeurs par polygone (clé = WKT du polygone, valeurs = liste des valeurs raster)
    polygon_data = {}

    # Parcourir chaque raster et extraire les pixels
    for i, tif_file in enumerate(tif_files):
        print(f"Traitement de {tif_file}...")
        raster = arcpy.Raster(tif_file)

        # Convertir le raster en numpy array (remplacer nodata par une valeur distincte, ex: -9999)
        nodata_value = raster.noDataValue or -9999  # Utiliser une valeur par défaut si nodataValue n'est pas défini
        raster_array = arcpy.RasterToNumPyArray(raster, nodata_to_value=nodata_value)

        # Obtenir les coordonnées des coins des pixels
        x_min, y_min = raster.extent.XMin, raster.extent.YMin
        x_max, y_max = raster.extent.XMax, raster.extent.YMax
        cell_size = raster.meanCellWidth

        # Parcourir les pixels et les associer à des polygones
        rows, cols = raster_array.shape
        for row in range(rows):
            for col in range(cols):
                value = raster_array[row, col]
                if value != nodata_value:  # Ignorer les pixels nodata
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

                    # Ajouter la valeur raster au dictionnaire
                    if polygon_wkt not in polygon_data:
                        polygon_data[polygon_wkt] = [None] * len(tif_files)
                    polygon_data[polygon_wkt][i] = value

    # Insérer les polygones et les valeurs agrégées dans la feature class
    with arcpy.da.InsertCursor(output_feature_class, ["SHAPE@"] + field_names) as cursor:
        for polygon_wkt, values in polygon_data.items():
            polygon = arcpy.FromWKT(polygon_wkt)
            cursor.insertRow([polygon] + values)

    print(f"Feature class combinée créée : {output_feature_class}")

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {end_time - start_time}")
