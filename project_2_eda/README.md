# Project 2 — Exploratory Data Analysis (EDA)

## Objectif
Analyser le dataset nettoyé (issu du Project 1) pour comprendre les
tendances, distributions et anomalies présentes dans les données.

## Fichiers
| Fichier | Description |
|---|---|
| `eda_project2.py` | Script Python (pandas/numpy) réalisant l'analyse exploratoire |
| `eda_summary.txt` | Résumé exécutif généré par le script |

> Le script utilise `Dataset_Cleaned.xlsx` produit par le Project 1
> (voir `../project_1_data_cleaning/`).

## Ce qui a été fait
- Statistiques descriptives (count, mean, median, std, min, max) sur les
  variables numériques
- Répartition des commandes par produit, méthode de paiement et statut
- Analyse de tendance : chiffre d'affaires par mois, top produits
- Détection des outliers par la méthode IQR (boxplot)
- Matrice de corrélation entre variables numériques
- Résumé exécutif ("So What?") avec les insights business clés

## Exécution
```bash
pip install pandas numpy openpyxl
python eda_project2.py
```

## Insight clé
Sur 1200 commandes analysées (CA total ≈ 1,26M), le produit **Chair**
génère le plus de revenu, la méthode de paiement **Online** domine
(21,5%), et 8 outliers ont été détectés sur `TotalPrice` — à investiguer
comme signal (grosses commandes légitimes) plutôt que comme bruit.
