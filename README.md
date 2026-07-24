# DecodeLabs — Data Analytics Internship Tasks

**Auteur :** Khaoula
**Batch :** 2026
**Programme :** Industrial Training Kit — DecodeLabs

Ce repo contient mes soumissions pour le programme de stage Data Analytics
chez DecodeLabs. Conformément au formulaire de soumission, j'ai complété
**3 tâches** sur les projets proposés, en respectant à chaque fois les
exigences et les seuils de qualité demandés dans le brief.

## 📁 Structure du repo

```
decodelabs_tasks/
│
├── project_1_data_cleaning/     # Project 1 : Data Cleaning & Preparation
│   ├── data_cleaning_project1.py
│   ├── Dataset_Raw.xlsx
│   ├── Dataset_Cleaned.xlsx
│   ├── change_log.csv
│   └── README.md
│
├── project_2_eda/               # Project 2 : Exploratory Data Analysis
│   ├── eda_project2.py
│   ├── eda_summary.txt
│   └── README.md
│
├── project_3_sql_analysis/      # Project 3 : SQL Data Analysis
│   ├── sql_project3.py
│   ├── sales.db
│   └── README.md
│
└── README.md                    # Ce fichier
```

## 🧩 Vue d'ensemble des projets

| # | Projet | Compétences démontrées | Statut |
|---|---|---|---|
| 1 | **Data Cleaning & Preparation** | pandas, gestion des valeurs manquantes, déduplication, standardisation de formats | ✅ Terminé |
| 2 | **Exploratory Data Analysis (EDA)** | statistiques descriptives, détection d'outliers (IQR), corrélation, storytelling avec les données | ✅ Terminé |
| 3 | **SQL Data Analysis** | SQL (SELECT, WHERE, GROUP BY, HAVING, agrégations), SQLite | ✅ Terminé |

Les trois projets s'enchaînent logiquement : le dataset brut est nettoyé
dans le **Project 1**, puis ce dataset propre (`Dataset_Cleaned.xlsx`) est
réutilisé comme point de départ pour le **Project 2** (analyse
exploratoire) et le **Project 3** (analyse SQL).

## 🛠️ Stack technique
- **Python** : pandas, numpy, sqlite3, openpyxl
- **SQL** : SQLite

## ▶️ Comment exécuter les projets

Chaque dossier de projet est autonome et contient son propre README avec
les instructions détaillées. En résumé :

```bash
pip install pandas numpy openpyxl

# Project 1
cd project_1_data_cleaning && python data_cleaning_project1.py

# Project 2 (nécessite Dataset_Cleaned.xlsx du Project 1)
cd ../project_2_eda && python eda_project2.py

# Project 3 (nécessite Dataset_Cleaned.xlsx du Project 1)
cd ../project_3_sql_analysis && python sql_project3.py
```

## 📊 Points clés à retenir

- **Qualité des données** : le dataset de départ (1200 commandes) ne
  présentait aucun doublon ni date mal formatée ; le seul problème réel
  était 309 valeurs manquantes sur `CouponCode`, traitées par imputation
  plutôt que par suppression de lignes.
- **Insight business principal** : le produit **Chair** génère le plus de
  chiffre d'affaires (~195 620), la méthode de paiement **Online** domine
  les commandes (21,5%), et le pic de CA a été enregistré en **juin 2024**.
- **Rigueur méthodologique** : chaque étape de nettoyage est tracée dans
  un change log, et chaque script inclut des contrôles de validation
  automatiques avant export.

## 📬 Contact
Pour toute question sur ce repo : engineerkhaoula@gmail.com

---
*Réalisé dans le cadre du programme Industrial Training Kit 2026 de DecodeLabs.*
