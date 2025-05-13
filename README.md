# 🏛️ ELEXXION

## 📋 SOMMAIRE

- [INTRODUCTION](#-introduction)  
- [STRUCTURE DOSSIERS](#-structure-dossiers)  
- [DONNÉES UTILISÉES](#-données-utilisées)  
- [DÉPENDANCES](#-dépendances)  

## 📦 INTRODUCTION

Ce projet a pour objectif de nettoyer, transformer et documenter les fichiers de l’Enquête Emploi en Continu (EEC) pour l’année 2023, dans le cadre d’un travail de préparation de données pour des analyses statistiques.  
Il s’appuie sur des scripts Python permettant de :  

- Lire et fusionner les fichiers source au format CSV
- Nettoyer les données en supprimant les colonnes vides ou constantes
- Protéger certaines variables sensibles selon les métadonnées (COD_VAR)
- Sauvegarder les jeux de données nettoyés au format Parquet
- Générer des logs de transformation ainsi que des rapports de valeurs uniques pour documentation et traçabilité

## 📂 STRUCTURE DOSSIERS

```bash
├── association/
│   ├── raw/
├── crime/
│   ├── raw/
├── election/
│   ├── raw/
├── emploi/
│   ├── data/
│   ├── metadata/
├── notebooks/
│   ├── elexxion-association.ipynb
│   ├── elexxion-crime.ipynb
│   ├── elexxion-election.ipynb
│   ├── elexxion-emploi.ipynb
├── .gitignore
├── README.md
```

## 📊 DONNÉES UTILISÉES

Les données utilisées proviennent de [www.data.gouv.fr](https://www.data.gouv.fr/fr/).  

**Lien vers les données** 👉  

- [Association](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/)  
- [Crime](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)  
- [Election](https://www.data.gouv.fr/fr/datasets/?q=election)  
- [Emploi et chômage](https://www.data.gouv.fr/fr/datasets/activite-emploi-et-chomage-enquete-emploi-en-continu/)  

## 📚 DÉPENDANCES

- Python >= 3.7
- pandas
- numpy
- pyarrow

Installez les dépendances si nécessaire :

```bash
pip install pandas numpy pyarrow
```
