# Project 1 — Data Cleaning & Preparation

## Objectif
Nettoyer un dataset e-commerce brut en traitant les valeurs manquantes, les
doublons et les formats incorrects, pour produire un dataset "Gold Standard"
prêt pour l'analyse.

## Fichiers
| Fichier | Description |
|---|---|
| `data_cleaning_project1.py` | Script Python (pandas) qui nettoie le dataset |
| `Dataset_Raw.xlsx` | Dataset brut d'entrée |
| `Dataset_Cleaned.xlsx` | Dataset nettoyé, produit par le script |
| `change_log.csv` | Journal des modifications appliquées (traçabilité) |

## Ce qui a été fait
- Identification et imputation des valeurs manquantes (`CouponCode` → `"No Coupon"`)
- Détection et suppression des doublons (lignes strictes + `OrderID`)
- Standardisation des formats : dates en ISO 8601 (`YYYY-MM-DD`), texte en
  trim + title case, IDs en majuscules, montants arrondis à 2 décimales
- Contrôle de cohérence métier : `TotalPrice == Quantity × UnitPrice`
- Validation finale automatisée (0% doublons sur `OrderID`, 0% dates mal
  formatées) avant export

## Exécution
```bash
pip install pandas openpyxl
python data_cleaning_project1.py
```

## Résultat clé
Dataset de 1200 commandes, 100% conforme au seuil de validation exigé par
le brief (0 doublon, 0 erreur de format de date).
