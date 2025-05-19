# Recréer le traitement combiné T1 et T2 en CSV à partir des fichiers Excel
import pandas as pd
# Recharger les fichiers Excel T1 et T2
xlsx_t1 = pd.ExcelFile("LEG_2017_T1.xlsx")
df_t1_raw = xlsx_t1.parse('Feuil1')

xlsx_t2 = pd.ExcelFile("LEG_2017_T2.xlsx")
df_t2_raw = xlsx_t2.parse('Feuil1')

# Colonnes fixes à conserver
fixed_columns = ['Code du département', 'Libellé du département', 'Inscrits', 'Abstentions']
start_idx = df_t1_raw.columns.get_loc('Code Nuance')
step = 5

# --- Extraction T1 ---
records_t1 = []
for _, row in df_t1_raw.iterrows():
    fixed_data = {col: row[col] for col in fixed_columns}
    for i in range(start_idx, len(df_t1_raw.columns), step):
        bloc = df_t1_raw.columns[i:i+step]
        if len(bloc) < 5:
            continue
        party_data = row[bloc]
        if pd.isna(party_data.iloc[0]):
            continue
        records_t1.append({
            'Code_departement': fixed_data['Code du département'],
            'Libelle_departement': fixed_data['Libellé du département'],
            'Code_Nuance': party_data.iloc[0],
            'Voix_T1': party_data.iloc[1],
            'pct_Voix_Ins_T1': party_data.iloc[2],
            'pct_Voix_Exp_T1': party_data.iloc[3],
            'Sieges_T1': party_data.iloc[4]
        })
df_t1 = pd.DataFrame(records_t1)

# --- Extraction T2 ---
records_t2 = []
for _, row in df_t2_raw.iterrows():
    fixed_data = {col: row[col] for col in fixed_columns}
    for i in range(start_idx, len(df_t2_raw.columns), step):
        bloc = df_t2_raw.columns[i:i+step]
        if len(bloc) < 5:
            continue
        party_data = row[bloc]
        if pd.isna(party_data.iloc[0]):
            continue
        records_t2.append({
            'Code_departement': fixed_data['Code du département'],
            'Libelle_departement': fixed_data['Libellé du département'],
            'Code_Nuance': party_data.iloc[0],
            'Voix_T2': party_data.iloc[1],
            'pct_Voix_Ins_T2': party_data.iloc[2],
            'pct_Voix_Exp_T2': party_data.iloc[3],
            'Sieges_T2': party_data.iloc[4]
        })
df_t2 = pd.DataFrame(records_t2)

# Fusionner T1 et T2
df_merged = pd.merge(df_t1, df_t2, how="outer", on=["Code_departement", "Libelle_departement", "Code_Nuance"])

# Remplacer NaN par 0
for col in ['Voix_T1', 'pct_Voix_Ins_T1', 'pct_Voix_Exp_T1', 'Sieges_T1',
            'Voix_T2', 'pct_Voix_Ins_T2', 'pct_Voix_Exp_T2', 'Sieges_T2']:
    df_merged[col] = df_merged[col].fillna(0)

# Export CSV combiné
output_combined_csv = "LEG_2017.csv"
df_merged.to_csv(output_combined_csv, index=False)

