import arcpy
import os
import csv
from datetime import datetime
import re
start_time = datetime.now()


input_folder = "2_intersect_tif_cleangdbcorr_all"
output_folder = input_folder.replace("2_", "4_") +"_csv"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
             re.search(rf".tif$", f)]
# tif_files=tif_files[:1]

input_tif=tif_files[0]
for input_tif in tif_files:

    print("start : " + input_tif)

    # Chemin vers le fichier CSV de sortie
    output_csv = os.path.join(output_folder,
                              os.path.basename(input_tif.replace('tif', 'csv')))

    # Charger le raster
    raster = arcpy.Raster(input_tif)

    # Obtenir des informations sur le raster
    cell_size = raster.meanCellWidth
    nodata_value = raster.noDataValue or -9999  # Valeur nodata par défaut
    extent = raster.extent

    # Convertir le raster en numpy array
    raster_array = arcpy.RasterToNumPyArray(raster, nodata_to_value=nodata_value)

    # Préparer le fichier CSV
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Écrire l'en-tête
        csv_writer.writerow(["Longitude", "Latitude", "Value"])

        # Parcourir les pixels
        rows, cols = raster_array.shape
        for row in range(rows):
            for col in range(cols):
                value = raster_array[row, col]
                if value != nodata_value:  # Ignorer les pixels nodata
                    # Calculer les coordonnées du centre du pixel
                    x = extent.XMin + (col + 0.5) * cell_size
                    y = extent.YMax - (row + 0.5) * cell_size
                    # Écrire les données dans le fichier CSV
                    csv_writer.writerow([x, y, value])

    print(f"Données exportées avec succès dans : {output_csv}")

print(f"Temps total d'exécution : {datetime.now() - start_time}")
