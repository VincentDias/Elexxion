import os
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# === Load data ===
df_features = pd.read_parquet(os.path.join("..", "platinum", "df_platinum_features.parquet"))
df_votes = pd.read_parquet(os.path.join("..", "election", "gold", "LEG_2022.parquet"))

# === Filter features for years 2018 to 2022 ===
df_features_filtered = df_features[df_features["ANNEE"].between(2018, 2022)]

# === Aggregate features per department (mean) ===
df_features_agg = (
    df_features_filtered
    .groupby("DEPARTEMENT")
    .mean(numeric_only=True)
    .reset_index()
)

# === Determine winning party per department ===
df_votes_2022 = df_votes[df_votes["Annee"] == 2022]

if "Code_departement" not in df_votes_2022.columns:
    raise ValueError("Column 'Code_departement' not found in vote data.")

# Get the party with the most votes per department
df_winners = (
    df_votes_2022
    .sort_values("Voix_T1", ascending=False)
    .groupby("Code_departement")
    .first()
    .reset_index()
    .loc[:, ["Code_departement", "Code_Nuance"]]
)
df_winners.rename(columns={"Code_departement": "DEPARTEMENT"}, inplace=True)

# === Regroup political families ===
def regrouper_nuances(nuance):
    if nuance in ["CEN", "UMP", "DVD", "PRV", "NCE", "ALLI", "LR"]:
        return "DROITE"
    elif nuance in ["RN", "EXD"]:
        return "EXTREME_DROITE"
    elif nuance in ["VEC", "ECO", "DVG", "FG", "SOC", "RDG", "NUP", "REG"]:
        return "GAUCHE"
    elif nuance in ["EXG"]:
        return "EXTREME_GAUCHE"
    elif nuance in ["DVC", "ENS"]:
        return "CENTRE"
    else:
        return "AUTRE"

df_winners["NUANCE_GROUPEE"] = df_winners["Code_Nuance"].apply(regrouper_nuances)

# === Merge features with labels ===
df_model = df_winners.merge(df_features_agg, on="DEPARTEMENT", how="inner")

# === Prepare dataset ===
X = df_model.drop(columns=["DEPARTEMENT", "Code_Nuance", "NUANCE_GROUPEE"])
y = df_model["NUANCE_GROUPEE"]

# === Encode grouped classes ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, stratify=y_encoded, random_state=42
)

# === Train model ===
model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
model.fit(X_train, y_train)

# === Predictions ===
y_pred = model.predict(X_test)

# === Decode labels for readability ===
y_test_labels = le.inverse_transform(y_test)
y_pred_labels = le.inverse_transform(y_pred)

# === Classification report ===
print(classification_report(y_test_labels, y_pred_labels))

# === Feature importances ===
importances = model.feature_importances_
feature_names = X.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title("Importance des variables pour la prédiction de la famille politique gagnante")
plt.xlabel("Importance")
plt.ylabel("Variable")
plt.tight_layout()
plt.show()
