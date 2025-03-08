import arcpy
import os
import csv
from datetime import datetime
import pandas as pd

start_time = datetime.now()

input_dir = "3_merge_intersect_tif_numpycleancorr_all"
output_dir = "4b_merge_intersect_tif_numpycleancorr_all_csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_ty = ["Pâturage_Moins", "Pâturage_Plus",
          "Prairie_Moins", "Prairie_Plus"]

for ty in all_ty:
    feature_class = os.path.join(input_dir,
                                 ty + "_output_combined.gdb",
                                 "combined_pixels")

    # Chemin pour le fichier CSV de sortie
    output_csv = os.path.join(output_dir,
                              ty + "_combined_pixels_with_coordinates.csv")

    # Liste des champs attributaires (exclure les champs géométriques)
    fields = [field.name for field in arcpy.ListFields(feature_class) if
              field.type != "Geometry"]

    # Ajouter des colonnes pour la longitude et la latitude
    fields.extend(["Longitude", "Latitude"])

    # Vérifier et ajouter les champs Longitude et Latitude à la feature class
    if not any(field.name == "Longitude" for field in arcpy.ListFields(feature_class)):
        arcpy.management.AddField(feature_class, "Longitude", "DOUBLE")
    if not any(field.name == "Latitude" for field in arcpy.ListFields(feature_class)):
        arcpy.management.AddField(feature_class, "Latitude", "DOUBLE")

    # Créer et écrire dans le fichier CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Écrire l'en-tête
        csv_writer.writerow(fields)

        # Lire et mettre à jour les données de la feature class
        with arcpy.da.UpdateCursor(feature_class, ["SHAPE@", "Longitude", "Latitude"] + fields[:-2]) as cursor:
            for row in cursor:
                geometry = row[0]  # Géométrie du polygone
                centroid = geometry.centroid  # Calculer le centroïde du polygone
                longitude = round(centroid.X, 1)  # Longitude
                latitude = round(centroid.Y, 1)  # Latitude

                # Mettre à jour les champs Longitude et Latitude
                row[1] = longitude
                row[2] = latitude

                # Ajouter les valeurs dans le CSV
                csv_writer.writerow(list(row[3:]) + [longitude, latitude])

                # Mettre à jour la ligne dans la feature class
                cursor.updateRow(row)

    print(f"Fichier CSV créé avec succès : {output_csv}")

print(f"Temps total d'exécution : {datetime.now() - start_time}")

# Combiner les fichiers CSV Plus et Moins
infilePlus = output_dir+'/Pâturage_Plus_combined_pixels_with_coordinates.csv'
dtP = pd.read_csv(infilePlus)
infileMoins = output_dir+'/Pâturage_Moins_combined_pixels_with_coordinates.csv'
dtM = pd.read_csv(infileMoins)
dt = pd.concat([dtM, dtP], ignore_index=True)

# Créer une colonne temporaire pour concaténer Longitude et Latitude
dt['tmp'] = dt['Longitude'].astype(str) + "_" + dt['Latitude'].astype(str)

# Identifier les doublons dans les coordonnées
duplicated_values = dt['tmp'][dt['tmp'].duplicated()]

# Filtrer les lignes avec les valeurs dupliquées
result = dt[dt['tmp'].isin(duplicated_values)]

print(result)

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {end_time - start_time}")
