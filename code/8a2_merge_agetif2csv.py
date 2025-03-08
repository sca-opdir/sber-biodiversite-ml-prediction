import os
import pandas as pd
from datetime import datetime
start_time = datetime.now()

# Dossier contenant les fichiers CSV
input_folder = "8a1_intersect_tif_cleanage_all_csv"


all_ty = ["Pâturage", "Prairie"]

for ty in all_ty:


    output_csv = os.path.join(input_folder, "merged_"+ty+".csv")

    # Liste des fichiers CSV dont le nom commence par "Pâturage_Moins"
    csv_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if
                 f.startswith(ty) and f.endswith(".csv")]

    # Initialisation d'une variable pour stocker le dataframe final
    merged_df = None

    for csv_file in csv_files:
        # Charger le fichier CSV dans un DataFrame
        df = pd.read_csv(csv_file)

        # Renommer la colonne "Value" avec le nom du fichier
        new_column_name = os.path.basename(csv_file).replace(".csv", "")
        df = df.rename(columns={"Value": new_column_name})

        # Si merged_df est vide, assigner directement le DataFrame actuel
        if merged_df is None:
            merged_df = df
        else:
            # Fusionner avec le dataframe final sur "Longitude" et "Latitude"
            merged_df = pd.merge(merged_df, df, on=["Longitude", "Latitude"],
                                 how="outer")

    # Sauvegarder le DataFrame fusionné dans un fichier CSV
    merged_df.to_csv(output_csv, index=False)
    print(f"Fichier CSV fusionné créé avec succès : {output_csv}")


print(f"Temps total d'exécution : {datetime.now() - start_time}")
