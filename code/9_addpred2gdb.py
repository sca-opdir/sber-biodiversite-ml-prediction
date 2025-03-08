import arcpy
import os
import csv
from datetime import datetime
from collections import Counter

start_time = datetime.now()

input_dir_pred = "kaggle_data"
input_dir_gdb = "7_merge_intersect_tif2pred_numpyclean_all"
output_dir = "9_pred_gdb"

# Créer le répertoire de sortie s'il n'existe pas
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all_ty = ["Pâturage"]#, "Prairie"]
ty="Pâturage"
for ty in all_ty:
    input_csv = os.path.join(input_dir_pred,
                             ty.replace("â", "") +
                             "_combined_pixels_with_coordinates_with_predlabels_2025-02-28_dropout_filteredWeirdCols.csv")
    assert os.path.exists(input_csv)
    feature_class = os.path.join(input_dir_gdb,
                                 ty + "_output_combined.gdb", "combined_pixels")

    # Charger les coordonnées du CSV
    csv_coordinates = {}
    with open(input_csv, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = (float(row["Longitude"]), float(row["Latitude"]))
            if key in csv_coordinates:
                print(f"Doublon trouvé : {key}")
            csv_coordinates[key] = row["predicted_label"]


    label_counts = Counter(csv_coordinates.values())
    print(label_counts)

    # Charger les coordonnées de la gdb
    gdb_coordinates = set()
    with arcpy.da.SearchCursor(feature_class, ["Longitude", "Latitude"]) as cursor:
        for row in cursor:
            gdb_coordinates.add((float(row[0]), float(row[1])))

## c est possible qu il y a des missing_in_csv car j enlève
    # les pixels où les variables env. manquent
    # mais missing_in_gdb doit  être nul
    # Vérifier que toutes les paires de la gdb sont présentes dans le CSV
    missing_in_csv = gdb_coordinates - set(csv_coordinates.keys())
    if missing_in_csv:
        #print(f"Attention : certaines paires Longitude-Latitude sont absentes du CSV pour {ty}: {missing_in_csv}")
        print("!!! WARNING : # missing in csv : " + str(len(missing_in_csv)))

    else:
        print(f"Toutes les paires Longitude-Latitude de la gdb sont présentes dans le CSV pour {ty}.")

    # Vérifier que toutes les paires de la gdb sont présentes dans le CSV
    missing_in_gdb = csv_coordinates.keys() - set(gdb_coordinates)
    #assert len(missing_in_gdb) == 0
    if missing_in_gdb:
        print(f"Attention : certaines paires Longitude-Latitude sont absentes de la gdb pour {ty}: {missing_in_csv}")
    else:
        print(f"Toutes les paires Longitude-Latitude du CSV sont présentes dans la gdb pour {ty}.")

    # Créer une copie de la gdb initiale
    output_gdb = os.path.join(output_dir, ty + "_output_combined_with_predlabels.gdb")
    if not arcpy.Exists(output_gdb):
        arcpy.management.CreateFileGDB(output_dir, ty + "_output_combined_with_predlabels.gdb")
    copied_feature_class = os.path.join(output_gdb, "combined_pixels_withpred")
    arcpy.management.Copy(feature_class, copied_feature_class)

    # Jointure pour ajouter le champ "predicted_label"
    arcpy.management.AddField(copied_feature_class, "predicted_label", "TEXT")
    with arcpy.da.UpdateCursor(copied_feature_class, ["Longitude", "Latitude", "predicted_label"]) as cursor:
        for row in cursor:
            key = (float(row[0]), float(row[1]))
            if key in csv_coordinates:
                row[2] = csv_coordinates[key]  # Ajouter la valeur "predicted_label"
                cursor.updateRow(row)

    print(f"Le champ 'predicted_label' a été ajouté à la gdb pour {ty}.")

end_time = datetime.now()
print(f"Script exécuté en {end_time - start_time}")
