import pandas as pd
import os
import re

input_dir = os.path.join("..", "..", "election", "raw")
output_dir = os.path.join("..", "..", "election", "bronze")
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".csv"):
        match = re.search(r"(\d{4})", file)
        year = match.group(1) if match else "XXXX"

        # Lire avec dtype explicite
        df = pd.read_csv(
            os.path.join(input_dir, file),
            dtype={"Code du département": str},  # <-- ici
            low_memory=False
        )

        df["Annee"] = int(year)
        df.to_parquet(os.path.join(output_dir, f"LEG_{year}.parquet"), index=False)
        print(f"[✓] Bronze écrit : LEG_{year}.parquet")
