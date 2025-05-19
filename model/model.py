import os.path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error

# 1. Chargement
df_gold = pd.read_parquet(os.path.join("..", "election", "gold", "LEG_2022.parquet"))
df_platine = pd.read_parquet(os.path.join("..", "platinum", "df_platinum_features.parquet"))

# 2. Fusion
df = pd.merge(df_gold, df_platine, how="inner", left_on=["Code_departement", "Annee"], right_on=["DEPARTEMENT", "ANNEE"])

# 3. Définir X et y
X = df[["Code_Nuance", "POPULATION", "TAUX_CHOMAGE", "NOMBRE", "NOMBRE_NOUVELLE_ASSO", "REGION", "ANNEE"]]
y = df["pct_Voix_Ins_T1"]

# 4. Prétraitement
categorical_features = ["Code_Nuance", "REGION"]
numerical_features = ["POPULATION", "TAUX_CHOMAGE", "NOMBRE", "NOMBRE_NOUVELLE_ASSO", "ANNEE"]

preprocessor = ColumnTransformer(transformers=[
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
    ]), numerical_features),

    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# 6. Évaluation
y_pred = pipeline.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
