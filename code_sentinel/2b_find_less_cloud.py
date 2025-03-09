import os
from datetime import datetime
import arcpy
import pandas as pd
import numpy as np
import re


start_time = datetime.now()

infold = "2_intersect_tif_cleangdbcorr_all"

pattern = re.compile(r"^Pâturage_Plus.+cloudproba.+\.tif$")

# Filtrer les fichiers correspondant au pattern

all_tifs = [os.path.join(infold, x) for x in os.listdir(infold)]
# cp_tifs = [x for x in all_tifs if "cloudproba" in os.path.basename(x)]
# cp_tifs = [x for x in cp_tifs if "Pâturage_Plus" in os.path.basename(x)]
cp_tifs = [x for x in all_tifs if pattern.match(os.path.basename(x))]

all_means = dict()

tif_path=cp_tifs[0]
for tif_path in cp_tifs:

    print("> start " + os.path.basename(tif_path))

    # Utiliser arcpy pour lire les valeurs du raster
    raster = arcpy.Raster(tif_path)

    # Obtenir les dimensions du raster
    rows = raster.height
    cols = raster.width

    # Obtenir les valeurs sous forme de numpy array
    array = arcpy.RasterToNumPyArray(raster, nodata_to_value=0)

    all_means[tif_path] = np.mean(array)

# # Créer une liste de tuples pour stocker les données avec les coordonnées
# data = []
# lower_left = raster.extent.lowerLeft  # Coordonnée du coin inférieur gauche
# cell_size = raster.meanCellWidth  # Taille des pixels
#
# # Convertir les valeurs du raster en DataFrame avec les coordonnées X, Y
# for r in range(rows):
#     for c in range(cols):
#         x = lower_left.X + (c * cell_size) + (cell_size / 2)
#         y = lower_left.Y + (r * cell_size) + (cell_size / 2)
#         value = array[r, c]
#         data.append((x, y, value))
#
# # Convertir en DataFrame pandas
# df = pd.DataFrame(data, columns=["X", "Y", "Value"])
#
# # Afficher les premières lignes du DataFrame
# print(df.head())
#
# # Optionnel : Sauvegarder en CSV
# df.to_csv("output_raster_values.csv", index=False)

