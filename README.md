# Projet Elexxion - Nettoyage et transformation des données EEC

Ce projet a pour objectif de nettoyer, transformer et documenter les fichiers de l’Enquête Emploi en Continu (EEC) pour l’année 2023, dans le cadre d’un travail de préparation de données pour des analyses statistiques.

## 📦 Contenu du projet

- Scripts Python sous Google Colab pour :

  - Lire et fusionner les fichiers CSV
  - Nettoyer les colonnes vides et constantes
  - Protéger certaines colonnes critiques selon les métadonnées (`COD_VAR`)
  - Sauvegarder les jeux de données au format Parquet
  - Générer des logs de transformation et des logs des valeurs uniques

- 📂 Structure des dossiers :

```bash
├── emploi/
│   ├── datas/
│   │   ├── FD_csv_EEC23.csv
│   ├── metadatas/
│   │   ├── Varmod_EEC_2023.csv
├── notebooks/
│   ├── elexxion-emploi.ipynb
├── .gitignore
├── README.md
```

## 📊 Données utilisées

Les données utilisées proviennent de [www.data.gouv.fr](https://www.data.gouv.fr/fr/), "Activité emploi et chômage - enquête emploi en continu"  
Merci de télécharger les fichiers sources et de les placer dans le dossier approprié :

👉 **Lien vers les données** :  

- [Emploi et chômage](https://www.data.gouv.fr/fr/datasets/activite-emploi-et-chomage-enquete-emploi-en-continu/)  
- [Crime](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)  

**Format CSV [Format CSV](https://static.data.gouv.fr/resources/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/20250327-120914/donnee-dep-data.gouv-2024-geographie2024-produit-le2025-03-14.csv)**


## ⚙️ Dépendances

- Python >= 3.7
- pandas
- numpy
- pyarrow
- google.colab (si utilisé sur Colab)

Installez les dépendances si nécessaire :

```bash
pip install pandas numpy pyarrow
```

🚀 Exécution 1. TODO
