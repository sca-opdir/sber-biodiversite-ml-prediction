import arcpy
import os
from datetime import datetime

start_time = datetime.now()

# Définir les chemins des feature classes
fc_to_intersect = "5_output_praipat_age_clean/age_epdir_praipat.gdb/Pâturage_age_nevereval_praipat"
fc_with_labels = "9_pred_gdb/Pâturage_output_combined_with_predlabels.gdb/combined_pixels_withpred"
output_gdb = "11_output_praipat_age_clean/age_epdir_praipat.gdb"
output_intersect = os.path.join(output_gdb, "intersection_result")

# arcpy.Exists(fc_to_intersect)
# arcpy.Exists(fc_with_labels)

# Vérifier si le fichier intersect existe déjà et le supprimer
if arcpy.Exists(output_intersect):
    arcpy.management.Delete(output_intersect)
    print(f"{output_intersect} supprimé avec succès.")


# if arcpy.Exists(output_intersect) :
#     # Effectuer une intersection
arcpy.analysis.Intersect(
    in_features=[fc_to_intersect, fc_with_labels],
    out_feature_class=output_intersect,
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)
print(f"Intersection effectuée et enregistrée dans : {output_intersect}")

# Ajouter des champs pour les pourcentages
arcpy.management.AddField(fc_to_intersect, "Pct_PâtPlus", "DOUBLE")
arcpy.management.AddField(fc_to_intersect, "Pct_PâtMoins", "DOUBLE")
arcpy.management.AddField(fc_to_intersect, "Pct_Lab", "TEXT")

print("Champs Pct_PâtPlus et Pct_PâtMoins ajoutés.")

# Créer un dictionnaire pour stocker les aires
area_dict = {}

# Calculer les aires des polygones dans la feature class intersectée
with arcpy.da.SearchCursor(output_intersect, ["FID_Pâturage_age_nevereval_praipat",
                                              "predicted_label", "SHAPE@AREA"]) as cursor:
    for row in cursor:
        fid = row[0]
        predicted_label = row[1]
        area = row[2]
        if fid not in area_dict:
            area_dict[fid] = {"PâtPlus": 0, "PâtMoins": 0}
        if predicted_label == "PâtPlus":
            area_dict[fid]["PâtPlus"] += area
        elif predicted_label == "PâtMoins":
            area_dict[fid]["PâtMoins"] += area

# Déterminer le nom du champ d'identifiant unique
oid_field = arcpy.Describe(fc_to_intersect).oidFieldName
print("Champ d'identifiant unique :", oid_field)

# Utilisez ce champ dans les curseurs
with arcpy.da.UpdateCursor(fc_to_intersect, [oid_field, "SHAPE@AREA",
                                             "Pct_PâtPlus", "Pct_PâtMoins", "Pct_Lab"]) as cursor:
    for row in cursor:
        fid = row[0]
        total_area = row[1]
        if fid in area_dict:
            pâtplus_area = area_dict[fid]["PâtPlus"]
            pâtmoins_area = area_dict[fid]["PâtMoins"]
            pct_patplus = (pâtplus_area / total_area) * 100 if total_area > 0 else 0
            pct_patmoins = (pâtmoins_area / total_area) * 100 if total_area > 0 else 0
            row[2] = pct_patplus
            row[3] = pct_patmoins
            assert not (pct_patplus > 50 and pct_patmoins > 50)
            row[4] = "NA"
            if pct_patplus > 50 :
                row[4] = "PâtPlus"
            if pct_patmoins > 50 :
                row[4] = "PâtMoins"
        else:
            row[2] = 0
            row[3] = 0
            row[4] = "NA"
        cursor.updateRow(row)

fields = arcpy.ListFields(fc_to_intersect)

# Affiche les informations sur les champs
for field in fields:
    print(f"Nom : {field.name}, Type : {field.type}, Alias : {field.aliasName}")

# # Calculer les pourcentages
# with arcpy.da.UpdateCursor(fc_to_intersect, ["FID", "SHAPE@AREA", "Pct_PâtPlus", "Pct_PâtMoins"]) as cursor:
#     for row in cursor:
#         fid = row[0]
#         total_area = row[1]
#         if fid in area_dict:
#             pâtplus_area = area_dict[fid]["PâtPlus"]
#             pâtmoins_area = area_dict[fid]["PâtMoins"]
#             row[2] = (pâtplus_area / total_area) * 100 if total_area > 0 else 0
#             row[3] = (pâtmoins_area / total_area) * 100 if total_area > 0 else 0
#         else:
#             row[2] = 0
#             row[3] = 0
#         cursor.updateRow(row)

print("Les pourcentages ont été calculés et ajoutés à la table attributaire.")

end_time = datetime.now()
print(f"** END {start_time} - {end_time}")
print(f"Script exécuté en {end_time - start_time}")