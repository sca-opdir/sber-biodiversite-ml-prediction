username = "gablep"
password = "epDir2020"

import sys
from arcgis.gis import GIS
import arcpy
import os
from datetime import datetime

start_time = datetime.now()

# Paramètres
current_date = datetime.now().strftime('%Y-%m-%d')
output_folder = os.path.realpath("5_output_praipat_age_clean")
outgdb_name = f'age_epdir_praipat.gdb'
outfc1 = 'age_all_praipat'
outfc2 = 'age_nevereval_praipat'
outfc3 = 'Prairie_age_nevereval_praipat'
outfc4 = 'Pâturage_age_nevereval_praipat'
ctrled_fc = 'CONTROLE_Q2.gdb/CONTROLE_QII_SYNTHESE_SURF_EXPL'
codes_prai = [611, 612, 635]
codes_pat = [617, 618]
codes_ctrled = codes_prai + codes_pat

# Création du dossier de sortie
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Création de la geodatabase de sortie
output_gdb = os.path.join(output_folder, outgdb_name)
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(output_folder, outgdb_name)

# Connexion au portail
portal_url = "https://sit.vs.ch/portal/"
gis = GIS(portal_url, username, password, use_gen_token=True)
print("Logged in as: " + gis.properties.user.username)

# Récupération de la couche hébergée
surflayers = gis.content.search(query='title:"epdir_surface_exploitee"', item_type="Feature Layer")
surfexp_layer = [layer for layer in surflayers if layer.title == "epdir_surface_exploitee"]
assert len(surfexp_layer) == 1
layit = surfexp_layer[0]
fc = layit.layers[0]

# Téléchargement des entités dans la geodatabase
local_fc = os.path.join(output_gdb, "epdir_surface_exploitee")
print("Téléchargement des entités...")

# Utiliser .query() pour récupérer les entités
features = fc.query(where="1=1", out_fields="*", return_geometry=True)

# Sauvegarder les entités dans la geodatabase
features.save(output_gdb, "epdir_surface_exploitee")
print(f"Couche téléchargée et enregistrée dans la GDB : {local_fc}")

# Vérification des champs dans la couche locale
fc_fields = [field.name for field in arcpy.ListFields(local_fc)]
assert 'code_culture' in fc_fields, "Le champ 'code_culture' est manquant dans la couche 'fc'"
print(f"Champs dans la couche locale : {fc_fields}")

# Filtrer pour prendre seulement les polygones où 'code_culture' est dans codes_ctrled
filtered_fc = os.path.join(output_gdb, outfc1)
query = f"code_culture IN ({','.join(map(str, codes_ctrled))})"
arcpy.management.MakeFeatureLayer(local_fc, "filtered_layer", query)
arcpy.management.CopyFeatures("filtered_layer", filtered_fc)
print(f"Feature class filtrée créée : {filtered_fc}")

# Fonction pour supprimer une couche temporaire si elle existe
def delete_layer_if_exists(layer_name):
    if arcpy.Exists(layer_name):
        arcpy.management.Delete(layer_name)

# Création d'une couche temporaire pour la feature class à traiter
delete_layer_if_exists("filtered_layer")
arcpy.management.MakeFeatureLayer(filtered_fc, "filtered_layer")

delete_layer_if_exists("ctrled_layer")
arcpy.management.MakeFeatureLayer(ctrled_fc, "ctrled_layer")

# Sélection des polygones de filtered_fc qui ne se chevauchent pas avec ctrled_fc
arcpy.management.SelectLayerByLocation(
    in_layer="filtered_layer",
    overlap_type="INTERSECT",
    select_features="ctrled_layer",
    selection_type="NEW_SELECTION"
)

# Inverser la sélection pour ne garder que les polygones sans chevauchement
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="filtered_layer",
    selection_type="SWITCH_SELECTION"
)

# Sauvegarder les polygones restants dans une nouvelle feature class
diff_fc = os.path.join(output_gdb, outfc2)
arcpy.management.CopyFeatures("filtered_layer", diff_fc)
print(f"Feature class des polygones sans chevauchement créée : {diff_fc}")

# Sous-ensemble Prairie (codes 611, 612, 635)
prairie_query = "code_culture IN (611, 612, 635)"
prairie_fc = os.path.join(output_gdb, outfc3)
arcpy.management.MakeFeatureLayer(diff_fc, "prairie_layer", prairie_query)
arcpy.management.CopyFeatures("prairie_layer", prairie_fc)
print(f"Feature class Prairie créée : {prairie_fc}")

# Sous-ensemble Pâturage (codes 617, 618)
paturage_query = "code_culture IN (617, 618)"
paturage_fc = os.path.join(output_gdb, outfc4)
arcpy.management.MakeFeatureLayer(diff_fc, "paturage_layer", paturage_query)
arcpy.management.CopyFeatures("paturage_layer", paturage_fc)
print(f"Feature class Pâturage créée : {paturage_fc}")

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {datetime.now() - start_time}")
