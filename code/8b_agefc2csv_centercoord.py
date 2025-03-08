import arcpy
import os
import csv
from datetime import datetime

start_time = datetime.now()

input_dir = "7_merge_intersect_tif2pred_numpyclean_all"
output_dir = "8b_merge_intersect_tif2pred_numpyclean_all_csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_ty = ["Pâturage", "Prairie"]

for ty in all_ty:
    feature_class = os.path.join(input_dir, ty + "_output_combined.gdb",
                                 "combined_pixels")

    # Ajouter des champs Longitude et Latitude à la table attributaire s'ils n'existent pas
    for field_name in ["Longitude", "Latitude"]:
        if field_name not in [f.name for f in arcpy.ListFields(feature_class)]:
            arcpy.management.AddField(feature_class, field_name, "DOUBLE")

    # Chemin pour le fichier CSV de sortie
    output_csv = os.path.join(output_dir, ty + "_combined_pixels_with_coordinates.csv")

    # Liste des champs attributaires, y compris Longitude et Latitude
    fields = [field.name for field in arcpy.ListFields(feature_class) if field.type != "Geometry"]

    # Mise à jour de la table attributaire pour calculer Longitude et Latitude
    with arcpy.da.UpdateCursor(feature_class, ["SHAPE@", "Longitude", "Latitude"]) as cursor:
        for row in cursor:
            geometry = row[0]  # Géométrie de l'entité
            if geometry:  # Si la géométrie existe
                centroid = geometry.centroid  # Calculer le centroïde
                row[1] = round(centroid.X, 6)  # Longitude
                row[2] = round(centroid.Y, 6)  # Latitude
            else:  # Si la géométrie est manquante
                row[1] = None
                row[2] = None
            cursor.updateRow(row)  # Mettre à jour la table attributaire

    print(f"Longitude et Latitude ajoutées dans la table attributaire de {ty}.")

    # Génération du fichier CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Écrire l'en-tête
        csv_writer.writerow(fields)

        # Lire les données de la feature class et écrire dans le CSV
        with arcpy.da.SearchCursor(feature_class, fields) as cursor:
            for row in cursor:
                csv_writer.writerow(row)

    print(f"Fichier CSV créé avec succès : {output_csv}")

print(f"Temps total d'exécution : {datetime.now() - start_time}")



# import arcpy
# import os
# import csv
# from datetime import datetime
# start_time = datetime.now()
#
# input_dir = "merge_intersect_tif2pred_numpyclean_all"
#
# output_dir = "merge_intersect_tif2pred_numpyclean_all_csv"
#
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
#
#
# all_ty = ["Pâturage",
#           "Prairie"]
#
# for ty in all_ty:
#     feature_class = os.path.join(input_dir,
#                                  ty+"_output_combined.gdb",
#                     "combined_pixels")
#
#     # Chemin pour le fichier CSV de sortie
#     output_csv = os.path.join(output_dir,
#                               ty + "_combined_pixels_with_coordinates.csv")
#
#     # Liste des champs attributaires (exclure les champs géométriques)
#     fields = [field.name for field in arcpy.ListFields(feature_class) if
#               field.type != "Geometry"]
#
#     # Ajouter des colonnes pour la longitude et la latitude
#     fields.extend(["Longitude", "Latitude"])
#
#     # Créer et écrire dans le fichier CSV
#     with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
#         csv_writer = csv.writer(csv_file)
#
#         # Écrire l'en-tête
#         csv_writer.writerow(fields)
#
#         # Lire les données de la feature class
#         with arcpy.da.SearchCursor(feature_class, ["SHAPE@"] + fields[:-2]) as cursor:
#             for row in cursor:
#                 geometry = row[0]  # Géométrie du polygone
#                 centroid = geometry.centroid  # Calculer le centroïde du polygone
#                 longitude = round(centroid.X,1) # Longitude
#                 latitude = round(centroid.Y,1)  # Latitude
#
#                 # Ajouter les valeurs des colonnes Longitude et Latitude
#                 csv_writer.writerow(list(row[1:]) + [longitude, latitude])
#
#     print(f"Fichier CSV créé avec succès : {output_csv}")
#
# print(f"Temps total d'exécution : {datetime.now() - start_time}")
