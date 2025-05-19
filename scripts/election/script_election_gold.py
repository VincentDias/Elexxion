import pandas as pd
import os
import re

input_dir = os.path.join("..", "..", "election", "silver")
output_dir = os.path.join("..", "..", "election", "gold")
os.makedirs(output_dir, exist_ok=True)

keep_cols = [
    "Code_departement", "Libelle_departement", "Code_Nuance",
    "Voix_T1", "pct_Voix_Ins_T1", "pct_Voix_Exp_T1",
    "Voix_T2", "pct_Voix_Ins_T2", "pct_Voix_Exp_T2",
    "Annee"
]

for file in os.listdir(input_dir):
    if file.endswith(".parquet"):
        match = re.search(r"(\d{4})", file)
        year = match.group(1) if match else "XXXX"
        df = pd.read_parquet(os.path.join(input_dir, file))
        df["Annee"] = int(year)  # Sécurité
        df_final = df[keep_cols]
        df_final.to_parquet(os.path.join(output_dir, f"LEG_{year}.parquet"), index=False)
        print(f"[✓] Gold écrit : LEG_{year}.parquet")
