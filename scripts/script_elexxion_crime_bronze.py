import os
import pandas as pd
import re
import s3fs
from dotenv import load_dotenv

load_dotenv()


# Chargement des variables d'environnement
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USER = os.getenv("MINIO_ROOT_USER")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

fs = s3fs.S3FileSystem(
  key=MINIO_USER,
  secret=MINIO_PASSWORD,
  client_kwargs={"endpoint_url": f"http://{MINIO_ENDPOINT}"}
)

storage_opts = {
  "key": MINIO_USER,
  "secret": MINIO_PASSWORD,
  "client_kwargs": {"endpoint_url": f"http://{MINIO_ENDPOINT}"}
}

all_paths = fs.find(f"{MINIO_BUCKET}/raw/crime")

csv_paths = [
  p for p in all_paths
  if re.search(r"crime_2016_2024_departement.*\.csv$", p)
]
if not csv_paths:
  raise FileNotFoundError("Aucun fichier crime_2016_2024_departement*.csv trouvé sous raw/crime")

csv_key = csv_paths[0]
print("📚 CSV file detected :", csv_key)

df = pd.read_csv(
  f"s3://{csv_key}",
  sep=";",
  dtype=str,
  storage_options=storage_opts
)

parquet_key = (
  f"{MINIO_BUCKET}/output/bronze/crime/"
  f"df_bronze_crime_2016_2024_departement.parquet"
)
df.to_parquet(
  f"s3://{parquet_key}",
  index=False,
  storage_options=storage_opts
)

print(f"🧬 Convert in parquet and stocked in s3://{parquet_key}")
