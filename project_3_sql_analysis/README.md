# Project 3 — SQL Data Analysis

## Objectif
Utiliser des requêtes SQL pour extraire des insights business à partir du
dataset nettoyé, en maîtrisant `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`
et les agrégations de base (`COUNT`, `SUM`, `AVG`).

## Fichiers
| Fichier | Description |
|---|---|
| `sql_project3.py` | Script Python qui charge le dataset dans SQLite et exécute les requêtes SQL |
| `sales.db` | Base SQLite générée (table `orders`) |

## Requêtes couvertes
1. `SELECT` + `WHERE` — commandes livrées de plus de 1000
2. `GROUP BY` + `COUNT`/`SUM`/`AVG` — CA et panier moyen par produit
3. `GROUP BY` + `ORDER BY` — répartition des méthodes de paiement (%)
4. `HAVING` (bonus) — produits dont le CA dépasse un seuil, filtré sur un
   agrégat
5. Analyse temporelle avec `strftime` — CA par mois
6. `WHERE ... IN (...)` + `ORDER BY` — top commandes annulées/retournées

## Exécution
```bash
pip install pandas openpyxl
python sql_project3.py
```

Vous pouvez aussi interroger `sales.db` directement avec n'importe quel
client SQLite (ex. `sqlite3 sales.db` en ligne de commande, ou DB Browser
for SQLite).

## Insight clé
Le produit **Chair** est en tête du classement CA (`GROUP BY` + `HAVING`),
et le mois de **juin 2024** enregistre le pic de chiffre d'affaires sur
les 30 mois analysés.
