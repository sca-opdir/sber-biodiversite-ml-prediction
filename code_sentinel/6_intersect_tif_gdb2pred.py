import os
import pandas as pd
import arcpy
from datetime import datetime
from arcpy.sa import ExtractByMask
import re
start_time = datetime.now()

## c est la version finale -> j output suelement les tif
# et ensuite dnas un 2ème script je combine les tif
# cela permet d éviter que les pixel fusionnent

q2ty = "Prairie"
sty = ""

gdb_path = "../SBER_IA/5_output_praipat_age_clean/age_epdir_praipat.gdb"
outfolder = "6_intersect_tif_cleanage_all"

data_folder = '../SBER_IA/data/swiss-eo'

keep_patt = re.compile(r".+2024-08-06.+bands-10m")

tif_files = os.listdir(data_folder)


tif_files = [os.path.join(data_folder,x) for x in tif_files if keep_patt.match(os.path.basename(x))]

assert len(tif_files) == 1  # Vérification qu'un seul raster correspond


q2ty="Pâturage"
sty="Plus"
input_tif = tif_files[0]
for input_tif in tif_files:

    for q2ty in ['Pâturage', "Prairie"]:
        # for sty in [""]:

        print(os.path.basename(input_tif) + " - " + q2ty)# + " - " +sty)

        input_feature_class = gdb_path + '/'+q2ty+ "_age_nevereval_praipat"
        # input_feature_class = "CONTROLE_Q2.gdb/CONTROLE_QII_SYNTHESE_SURF_EXPL"  # Feature class des polygones
        # outfile = q2ty + "_"+sty+"_vs_"+ os.path.basename(input_tif)
        outfile = q2ty +  "_vs_" + os.path.basename(input_tif)
        output_tif = os.path.join(outfolder,outfile)
        output_excel = os.path.join(outfolder, outfile.replace(".tif", ".xlsx"))

        output_feature_class =outfile.replace(".tif", "")

        output_matrix_excel = os.path.join(outfolder,
                                           outfile.replace(".tif", "_matrix.xlsx"))

        if not os.path.exists(outfolder):
            os.makedirs(outfolder)
        if os.path.exists(output_tif):
            os.remove(output_tif)

        # Vérifier que l'extension Spatial Analyst est disponible
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
        else:
            raise RuntimeError("L'extension Spatial Analyst n'est pas disponible.")

        # Extraction des pixels dans les polygones
        extracted_raster = ExtractByMask(in_raster=input_tif,
                                         in_mask_data=input_feature_class)

        # Sauvegarder le raster extrait
        extracted_raster.save(output_tif)
        print(f"Raster extrait et enregistré dans : {output_tif}")

end_time = datetime.now()
print(f"{start_time} - {end_time}")
print(f"Temps total d'exécution : {datetime.now() - start_time}")

