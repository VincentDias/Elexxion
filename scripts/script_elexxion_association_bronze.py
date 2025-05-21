import os
import re
import pandas as pd
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

expected_fields = 23
delimiter = ";"
storage_opts = {
  "key": MINIO_USER,
  "secret": MINIO_PASSWORD,
  "client_kwargs": {"endpoint_url": f"http://{MINIO_ENDPOINT}"}
}

# Validation
raw_keys = fs.glob(f"{MINIO_BUCKET}/raw/association/*.csv")
for key in raw_keys:
  filename = os.path.basename(key)
  out_key = key.replace("/raw/association/", "/raw/association/valid/").replace(".csv", "_valid.csv")
  valid_lines = []
  error_lines = []

  with fs.open(key, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
      if len(line.strip().split(delimiter)) == expected_fields:
        valid_lines.append(line.strip())
      else:
        error_lines.append(i)
  with fs.open(out_key, "w", encoding="utf-8") as f:
    for l in valid_lines:
      f.write(l + "\n")

# Conversion
valid_keys = fs.glob(f"{MINIO_BUCKET}/raw/association/valid/*.csv")
for csv_key in valid_keys:
  filename = os.path.basename(csv_key)
  m = re.search(r"rna_import_(\d{8})_dpt_([0-9]{2}|[0-9]{3}|2A|2B|97[1-9][0-9])", filename)
  if not m:
    continue

  date_str = m.group(1)
  year = date_str[:4]
  dpt = m.group(2)

  print("📚 CSV file detected :", csv_key)

  df = pd.read_csv(
    f"s3://{csv_key}",
    sep=delimiter,
    dtype=str,
    storage_options=storage_opts
  )

  parquet_key = (
    f"{MINIO_BUCKET}/output/bronze/association/"
    f"df_bronze_association_{year}_dpt_{dpt}.parquet"
  )
  df.to_parquet(
    f"s3://{parquet_key}",
    index=False,
    storage_options=storage_opts
  )

  print(f"🧬 Convert in parquet and stocked in s3://{parquet_key}")
