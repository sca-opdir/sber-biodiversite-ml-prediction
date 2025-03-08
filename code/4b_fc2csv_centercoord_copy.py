import arcpy
import os
import csv
from datetime import datetime

import pandas as pd

start_time = datetime.now()

input_dir = "merge_intersect_tif_numpycleancorr_all"

output_dir = "merge_intersect_tif_numpycleancorr_all_csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


all_ty = ["Pâturage_Moins", "Pâturage_Plus",
          "Prairie_Moins", "Prairie_Plus"]

for ty in all_ty:
    feature_class = os.path.join(input_dir,
                                 ty+"_output_combined.gdb",
                    "combined_pixels")

    # Chemin pour le fichier CSV de sortie
    output_csv = os.path.join(output_dir,
                              ty + "_combined_pixels_with_coordinates.csv")

    # Liste des champs attributaires (exclure les champs géométriques)
    fields = [field.name for field in arcpy.ListFields(feature_class) if
              field.type != "Geometry"]

    # Ajouter des colonnes pour la longitude et la latitude
    fields.extend(["Longitude", "Latitude"])

    # Créer et écrire dans le fichier CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Écrire l'en-tête
        csv_writer.writerow(fields)

        # Lire les données de la feature class
        with arcpy.da.SearchCursor(feature_class, ["SHAPE@"] + fields[:-2]) as cursor:
            for row in cursor:
                geometry = row[0]  # Géométrie du polygone
                centroid = geometry.centroid  # Calculer le centroïde du polygone
                longitude = round(centroid.X,1) # Longitude
                latitude = round(centroid.Y,1)  # Latitude

                # Ajouter les valeurs des colonnes Longitude et Latitude
                csv_writer.writerow(list(row[1:]) + [longitude, latitude])

    print(f"Fichier CSV créé avec succès : {output_csv}")

print(f"Temps total d'exécution : {datetime.now() - start_time}")




infilePlus = 'merge_intersect_tif_numpycleancorr_all_csv/Pâturage_Plus_combined_pixels_with_coordinates.csv'
dtP = pd.read_csv(infilePlus)
infileMoins = 'merge_intersect_tif_numpycleancorr_all_csv/Pâturage_Moins_combined_pixels_with_coordinates.csv'
dtM = pd.read_csv(infileMoins)
dt = pd.concat([dtM, dtP], ignore_index=True)
# Créer une colonne temporaire pour concaténer Longitude et Latitude
dt['tmp'] = dt['Longitude'].astype(str) + "_" + dt['Latitude'].astype(str)

# temp_col = dt['Longitude'].astype(str) + "_" + dt['Latitude'].astype(str)
# assert not any(temp_col.duplicated())

duplicated_values = dt['tmp'][dt['tmp'].duplicated()]

# Filtrer les lignes avec les valeurs dupliquées
result = dt[dt['tmp'].isin(duplicated_values)]
result
