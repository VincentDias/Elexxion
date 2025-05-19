import pandas as pd
import os
import re

input_dir = os.path.join("..", "..", "election", "bronze")
output_dir = os.path.join("..", "..", "election", "silver")
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".parquet"):
        match = re.search(r"(\d{4})", file)
        year = match.group(1) if match else "XXXX"
        df = pd.read_parquet(os.path.join(input_dir, file))

        # Nettoyage
        df = df[df["Code_Nuance"].notna()]
        num_cols = [
            "Voix_T1", "pct_Voix_Ins_T1", "pct_Voix_Exp_T1", "Sieges_T1",
            "Voix_T2", "pct_Voix_Ins_T2", "pct_Voix_Exp_T2", "Sieges_T2"
        ]
        df[num_cols] = df[num_cols].fillna(0)

        df.to_parquet(os.path.join(output_dir, f"LEG_{year}.parquet"), index=False)
        print(f"[✓] Silver écrit : LEG_{year}.parquet")
