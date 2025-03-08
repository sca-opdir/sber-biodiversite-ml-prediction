import arcpy
import os
from datetime import datetime

start_time = datetime.now()


# Définir les chemins d'entrée et de sortie
input_gdb = "CONTROLE_Q2.gdb"
input_feature_class = os.path.join(input_gdb, "CONTROLE_QII_SYNTHESE_SURF_EXPL")
output_gdb = "CONTROLE_Q2_clean.gdb"
output_folder = "output_clean_gdb"

# Créer le dossier de sortie
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Créer ou remplacer la geodatabase de sortie
output_gdb_path = os.path.join(output_folder, output_gdb)
if arcpy.Exists(output_gdb_path):
    arcpy.management.Delete(output_gdb_path)
arcpy.management.CreateFileGDB(output_folder, output_gdb)
print(f"Geodatabase créée : {output_gdb_path}")

# Obtenir la projection de la feature class d'entrée
desc = arcpy.Describe(input_feature_class)
spatial_reference = desc.spatialReference
for cty in ["Prairie", "Pâturage","PPS"]:
#for cty in ["Prairie"]:
    # Définir les chemins des feature classes de sortie
    cty_fc = os.path.join(output_gdb_path, f"controleQ2_{cty}")
    cty_fc_nodup = os.path.join(output_gdb_path, f"controleQ2_{cty}_nodup")
    cty_fc_duplicates = os.path.join(output_gdb_path, f"controleQ2_{cty}_duplicates")

    # Sous-ensemble : Filtrage par "TYPE"
    cty_where_clause = f"TYPE LIKE '%{cty}%'"
    arcpy.management.MakeFeatureLayer(input_feature_class, f"temp_layer_{cty}")
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view=f"temp_layer_{cty}",
        selection_type="NEW_SELECTION",
        where_clause=cty_where_clause
    )
    arcpy.management.CopyFeatures(f"temp_layer_{cty}", cty_fc)
    print(f"Feature class '{cty}_subset' créée : {cty_fc}")
    arcpy.management.Delete(f"temp_layer_{cty}")


# Ajouter un champ temporaire "ANNEE_EFFECTIVE"
    arcpy.management.AddField(cty_fc, "ANNEE_EFFECTIVE", "LONG")
    with arcpy.da.UpdateCursor(cty_fc, ["ANNEE", "ANNEE_EFFECTIVE"]) as cursor:
        for row in cursor:
            row[1] = row[0] if row[0] is not None else 0
            cursor.updateRow(row)

    # Identifiez les doublons par géométrie
    processed_geometries = {}
    duplicates = []
    fields = ["OID@", "SHAPE@", "ANNEE_EFFECTIVE"] + [f.name for f in arcpy.ListFields(cty_fc) if f.type not in ["OID", "Geometry"]]
    with arcpy.da.SearchCursor(cty_fc, fields) as cursor:
        for row in cursor:
            geom_wkt = row[1].WKT
            if geom_wkt not in processed_geometries:
                processed_geometries[geom_wkt] = row
            else:
                if row[2] > processed_geometries[geom_wkt][2]:  # Garder celui avec ANNEE max
                    duplicates.append(processed_geometries[geom_wkt])
                    processed_geometries[geom_wkt] = row
                else:
                    duplicates.append(row)

    # Créer la feature class sans doublons
    arcpy.management.CreateFeatureclass(
        output_gdb_path, f"controleQ2_{cty}_nodup", "POLYGON", template=cty_fc, spatial_reference=spatial_reference
    )
    with arcpy.da.InsertCursor(cty_fc_nodup, fields) as cursor:
        for row in processed_geometries.values():
            cursor.insertRow(row)

    # Créer la feature class des doublons
    arcpy.management.CreateFeatureclass(
        output_gdb_path, f"controleQ2_{cty}_duplicates", "POLYGON", template=cty_fc, spatial_reference=spatial_reference
    )
    with arcpy.da.InsertCursor(cty_fc_duplicates, fields) as cursor:
        for row in duplicates:
            cursor.insertRow(row)

    print(f"Feature class sans doublons '{cty_fc_nodup}' créée.")
    print(f"Feature class des doublons '{cty_fc_duplicates}' créée.")


# Sous-ensemble : Filtrage par "QUALITE"
    for qty in ['Plus', 'Moins', 'Autre surface']:
#    for qty in ['Plus']:
        qtylab = qty.replace(" ", "")
        cty_fc_nodup_qty = os.path.join(output_gdb_path, f"controleQ2_{cty}_nodup_{qtylab}")
        qty_where_clause = f"QUALITE LIKE '%{qty}%'"
        arcpy.management.MakeFeatureLayer(cty_fc_nodup, f"temp_layer_{qtylab}")
        arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=f"temp_layer_{qtylab}",
            selection_type="NEW_SELECTION",
            where_clause=qty_where_clause
        )
        arcpy.management.CopyFeatures(f"temp_layer_{qtylab}", cty_fc_nodup_qty)
        print(f"Feature class '{cty}_subset' créée : {cty_fc_nodup_qty}")
        arcpy.management.Delete(f"temp_layer_{qtylab}")

    print(f"Feature class selon Qualité '{cty_fc_nodup_qty}' créée.")


end_time = datetime.now()
print(f"{start_time} - {end_time}")
