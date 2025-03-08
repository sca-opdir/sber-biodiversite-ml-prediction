import arcpy
import os
from datetime import datetime

start_time = datetime.now()

# Définir les chemins d'entrée et de sortie
input_gdb = "CONTROLE_Q2.gdb"
input_feature_class = os.path.join(input_gdb, "CONTROLE_QII_SYNTHESE_SURF_EXPL")
output_gdb = "CONTROLE_Q2_clean.gdb"
output_folder = "1_output_clean_gdbcorr"

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

for cty in ["Prairie", "Pâturage", "PPS"]:
    # Définir les chemins des feature classes de sortie
    cty_fc = os.path.join(output_gdb_path, f"controleQ2_{cty}")
    cty_fc_clean = os.path.join(output_gdb_path, f"controleQ2_{cty}_clean")

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

    # Vérifier la présence du champ "ANNEE" avant l'Union
    input_fields = [field.name for field in arcpy.ListFields(cty_fc)]
    if "ANNEE" not in input_fields:
        raise RuntimeError(f"Le champ 'ANNEE' est manquant dans la couche '{cty_fc}'.")

    # Découper les superpositions avec l'outil Union
    union_output = os.path.join(output_gdb_path, f"{cty}_union")
    arcpy.analysis.Union([cty_fc], union_output, "ALL")
    print(f"Polygones découpés par Union : {union_output}")

    # Supprimer une couche temporaire existante avant de la recréer
    if arcpy.Exists("union_layer"):
        arcpy.management.Delete("union_layer")

    # Supprimer les géométries vides résultant de l'Union
    valid_polygons = os.path.join(output_gdb_path, f"{cty}_valid_polygons")
    arcpy.management.MakeFeatureLayer(union_output, "union_layer")
    arcpy.management.SelectLayerByAttribute(
        "union_layer", "NEW_SELECTION", "Shape_Area > 0"
    )
    arcpy.management.CopyFeatures("union_layer", valid_polygons)
    arcpy.management.Delete("union_layer")  # Supprimer après utilisation
    print(f"Polygones valides extraits : {valid_polygons}")

    # Ajouter un champ pour trier par ANNEE
    arcpy.management.AddField(valid_polygons, "MAX_YEAR", "LONG")

    # Identifier et conserver les polygones avec l'année la plus récente
    with arcpy.da.UpdateCursor(valid_polygons, ["ANNEE", "MAX_YEAR"]) as cursor:
        for row in cursor:
            row[1] = row[0] if row[0] is not None else 0  # Copier l'année dans MAX_YEAR
            cursor.updateRow(row)

    # Trier et sélectionner les polygones uniques par emplacement
    arcpy.management.Sort(
        valid_polygons,
        cty_fc_clean,
        [["MAX_YEAR", "DESCENDING"]]
    )
    print(f"Feature class sans superposition créée : {cty_fc_clean}")

    # Sous-ensemble : Filtrage par "QUALITE"
    for qty in ['Plus', 'Moins', 'Autre surface']:
        qtylab = qty.replace(" ", "")
        cty_fc_clean_qty = os.path.join(output_gdb_path, f"controleQ2_{cty}_nodup_{qtylab}")
        qty_where_clause = f"QUALITE LIKE '%{qty}%'"
        arcpy.management.MakeFeatureLayer(cty_fc_clean, f"temp_layer_{qtylab}")
        arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=f"temp_layer_{qtylab}",
            selection_type="NEW_SELECTION",
            where_clause=qty_where_clause
        )
        arcpy.management.CopyFeatures(f"temp_layer_{qtylab}", cty_fc_clean_qty)
        arcpy.management.Delete(f"temp_layer_{qtylab}")
        print(f"Feature class '{cty_fc_clean_qty}' créée pour la qualité '{qty}'.")

end_time = datetime.now()
print(f"Temps total d'exécution : {end_time - start_time}")
