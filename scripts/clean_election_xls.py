# Colonnes fixes pour chaque département
fixed_columns = [
    'Code du département', 'Libellé du département', 'Inscrits', 'Abstentions'
]

# Commencer à la colonne d'index 17 où les blocs de partis débutent
start_idx = df.columns.get_loc('Code Nuance')
step = 5  # Chaque bloc de parti fait 5 colonnes

# Préparer une liste pour stocker les lignes finales
records = []

# Parcourir chaque ligne du fichier (chaque département)
for _, row in df.iterrows():
    # Extraire les informations fixes
    fixed_data = {col: row[col] for col in fixed_columns}

    # Parcourir les blocs de 5 colonnes pour chaque parti
    for i in range(start_idx, len(df.columns), step):
        bloc = df.columns[i:i + step]
        if len(bloc) < 5:
            continue  # ignorer les blocs incomplets
        party_data = row[bloc]
        if pd.isna(party_data.iloc[0]):
            continue  # ignorer si aucune donnée de nuance (donc pas de parti)

        record = {
            **fixed_data,
            'Code Nuance': party_data.iloc[0],
            'Voix': party_data.iloc[1],
            '% Voix/Ins': party_data.iloc[2],
            '% Voix/Exp': party_data.iloc[3],
            'Sièges': party_data.iloc[4]
        }
        records.append(record)

# Créer un DataFrame final
df_final = pd.DataFrame(records)

# Afficher le résultat
import ace_tools as tools;

tools.display_dataframe_to_user(name="Résultats par Parti et Département", dataframe=df_final)
