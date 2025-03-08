import arcpy
import os
import csv
from datetime import datetime

start_time = datetime.now()

input_dir_pred = "kaggle_data"
input_dir_gdb = "3_merge_intersect_tif_numpycleancorr_all"
output_dir = "10_trainpred_gdb"

# Créer le répertoire de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_ty = ["Pâturage"]
for ty in all_ty:
    output_gdb = os.path.join(output_dir, ty + "_output_combined_with_predlabels.gdb")
    # Créer une copie de la gdb initiale
    if not arcpy.Exists(output_gdb):
        arcpy.management.CreateFileGDB(output_dir, ty + "_output_combined_with_predlabels.gdb")

    input_csv = os.path.join(input_dir_pred,
                             ty.replace("â",
                                        "") +
                             "_MoinsPlus_combined_pixels_with_coordinates_with_predlabels_2025-02-28_dropout.csv")

    feature_class_plus = os.path.join(input_dir_gdb,
                                      ty + "_Plus_output_combined.gdb", "combined_pixels")
    feature_class_moins = os.path.join(input_dir_gdb,
                                       ty + "_Moins_output_combined.gdb", "combined_pixels")

    # Ajouter le champ 'true_label' à feature_class_plus et feature_class_moins
    if "true_label" not in [field.name for field in arcpy.ListFields(feature_class_plus)]:
        arcpy.management.AddField(feature_class_plus, "true_label", "TEXT")
        with arcpy.da.UpdateCursor(feature_class_plus, ["true_label"]) as cursor:
            for row in cursor:
                row[0] = "Plus"  # Définir la valeur pour chaque entité
                cursor.updateRow(row)

    if "true_label" not in [field.name for field in arcpy.ListFields(feature_class_moins)]:
        arcpy.management.AddField(feature_class_moins, "true_label", "TEXT")
        with arcpy.da.UpdateCursor(feature_class_moins, ["true_label"]) as cursor:
            for row in cursor:
                row[0] = "Moins"  # Définir la valeur pour chaque entité
                cursor.updateRow(row)

    # [field.name for field in arcpy.ListFields(feature_class_plus)]
    # [field.name for field in arcpy.ListFields(feature_class_moins)]
    # [field.name for field in arcpy.ListFields(combined_feature_class)]

    # Combiner les deux feature classes
    combined_feature_class = os.path.join(output_gdb, "combined_pixels")
    arcpy.management.Merge([feature_class_plus, feature_class_moins], combined_feature_class)
    print(f"Les classes d'entités 'Plus' et 'Moins' ont été combinées dans {combined_feature_class}")

    feature_class = combined_feature_class

    # Charger les coordonnées du CSV
    csv_coordinates = {}
    with open(input_csv, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = (float(row["Longitude"]), float(row["Latitude"]))
            csv_coordinates[key] = row["predicted_label"]

    # Charger les coordonnées de la gdb
    gdb_coordinates = set()
    with arcpy.da.SearchCursor(feature_class, ["Longitude", "Latitude"]) as cursor:
        for row in cursor:
            gdb_coordinates.add((float(row[0]), float(row[1])))

    missing_in_csv = gdb_coordinates - set(csv_coordinates.keys())
    if missing_in_csv:
        print("!!! WARNING : # missing in csv : " + str(len(missing_in_csv)))
    else:
        print(f"Toutes les paires Longitude-Latitude de la gdb sont présentes dans le CSV pour {ty}.")

    missing_in_gdb = csv_coordinates.keys() - set(gdb_coordinates)
    assert len(missing_in_gdb) == 0
    if missing_in_gdb:
        print(f"Attention : certaines paires Longitude-Latitude sont absentes de la gdb pour {ty}: {missing_in_csv}")
    else:
        print(f"Toutes les paires Longitude-Latitude du CSV sont présentes dans la gdb pour {ty}.")

    copied_feature_class = os.path.join(output_gdb, "combined_pixels_withpred")
    arcpy.management.Copy(feature_class, copied_feature_class)

    # Ajouter les champs 'predicted_label' et 'correct_pred'
    if "predicted_label" not in [field.name for field in arcpy.ListFields(copied_feature_class)]:
        arcpy.management.AddField(copied_feature_class, "predicted_label", "TEXT")

    if "correct_pred" not in [field.name for field in arcpy.ListFields(copied_feature_class)]:
        arcpy.management.AddField(copied_feature_class, "correct_pred", "TEXT")

    # Mettre à jour les champs dans une seule boucle
    with arcpy.da.UpdateCursor(copied_feature_class,
                               ["Longitude", "Latitude", "true_label", "predicted_label", "correct_pred"]) as cursor:
        for row in cursor:
            key = (float(row[0]), float(row[1]))  # Longitude, Latitude comme clé

            if key in csv_coordinates:  # Vérifier si les coordonnées existent dans le CSV
                pred_lab = csv_coordinates[key]
                row[3] = pred_lab.replace("Pât", "")  # Mettre à jour 'predicted_label'

                # Mettre à jour 'correct_pred' en comparant true_label et predicted_label
                if row[2] == row[3]:  # true_label correspond à predicted_label
                    row[4] = "True"
                else:
                    row[4] = "False"
            else:
                row[3] = None  # Si aucune prédiction n'est disponible
                row[4] = "False"  # On considère que c'est incorrect par défaut

            cursor.updateRow(row)


    # # Jointure pour ajouter le champ "predicted_label"
    # arcpy.management.AddField(copied_feature_class, "predicted_label", "TEXT")
    # with arcpy.da.UpdateCursor(copied_feature_class, ["Longitude", "Latitude", "predicted_label"]) as cursor:
    #     for row in cursor:
    #         key = (float(row[0]), float(row[1]))
    #         if key in csv_coordinates:
    #             row[2] = csv_coordinates[key]  # Ajouter la valeur "predicted_label"
    #             cursor.updateRow(row)
    # # [field.name for field in arcpy.ListFields(copied_feature_class)]

    print(f"Le champ 'predicted_label' et 'correct_pred' a été ajouté à la gdb pour {ty}.")

end_time = datetime.now()
print(f"** END {start_time} - {end_time}")
print(f"Script exécuté en {end_time - start_time}")
