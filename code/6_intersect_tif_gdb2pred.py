import os
import pandas as pd
import arcpy
from datetime import datetime
from arcpy.sa import ExtractByMask

start_time = datetime.now()

## c est la version finale -> j output suelement les tif
# et ensuite dnas un 2ème script je combine les tif
# cela permet d éviter que les pixel fusionnent

q2ty = "Prairie"
sty = ""

gdb_path = "5_output_praipat_age_clean/age_epdir_praipat.gdb"
outfolder = "6_intersect_tif_cleanage_all"

# output_gdb = outfolder + "/output.gdb"

all_tifs = [

"data/10635681_bioclim/chclim25/chclim25/present/1981_2010/tave/bioclim_chclim25_present_1981_2010_tave.tif",

# Prec
# (diff precipitation et annual precipit ?
"data/10635681_bioclim/chclim25/chclim25/present/1981_2010/prec/bioclim_chclim25_present_1981_2010_prec.tif",

# Evapotrans
"data/10635681_bioclim/chclim25/chclim25/present/1981_2010/etp/bioclim_chclim25_present_1981_2010_etp.tif",

# Growing day > 0
"data/10635681_bioclim/chclim25/chclim25/present/1981_2010/gdd0/bioclim_chclim25_present_1981_2010_gdd0.tif",
"data/10634975_rs/sdc/sdc/2017/ndvi/rs_sdc_2017_ndvi_mean.tif",
"data/10634975_rs/sdc/sdc/2017/ndwi/rs_sdc_2017_ndwi_mean.tif",
"data/10634975_rs/sdc/sdc/2021/lai/rs_sdc_2021_lai_mean.tif",
"data/10634975_rs/sdc/sdc/2021/gci/rs_sdc_2021_gci_mean.tif",
"data/10634975_rs/sdc/sdc/2021/evi/rs_sdc_2021_evi_mean.tif",

    # edaph/eiv - soil moisture
    "data/10635381_edaph/eiv/eiv/f/edaph_eiv_f.tif",
    # # edaph/eiv - soil humus
    "data/10635381_edaph/eiv/eiv/h/edaph_eiv_h.tif",
    # edaph/eiv -light
    "data/10635381_edaph/eiv/eiv/l/edaph_eiv_l.tif",
    # edaph/eiv - soil nutrients
    "data/10635381_edaph/eiv/eiv/n/edaph_eiv_n.tif",
    # edaph/eiv - soil ph
    "data/10635381_edaph/eiv/eiv/r/edaph_eiv_r.tif",
    # edaph/modiffus - N load
    'data/10635381_edaph/modiffus/modiffus/n/edaph_modiffus_n.tif',
    # # edaph/modiffus - P load
    'data/10635381_edaph/modiffus/modiffus/p/edaph_modiffus_p.tif',
    # # vege/nfi height of the vegetation canopy
    "data/10635551_vege/nfi/nfi/canopy/vege_nfi_canopy_median.tif",
    # topo/alti3d aspect=slope orientation
    "data/10635539_topo/alti3d/alti3d/aspect/topo_alti3d_aspect_median.tif",
    # topo/alti3d elevation [digital elevation model]
    "data/10635539_topo/alti3d/alti3d/dem/topo_alti3d_dem_median.tif",
    # # topo/alti3d slope
    "data/10635539_topo/alti3d/alti3d/slope/topo_alti3d_slope_median.tif",
    # topo/alti3d hillshade
    "data/10635539_topo/alti3d/alti3d/hillshade/topo_alti3d_hillshade_median.tif"
]



for tif_file in all_tifs:
    assert os.path.exists(tif_file)

q2ty="Pâturage"
sty="Plus"
input_tif = all_tifs[0]
for input_tif in all_tifs:

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

