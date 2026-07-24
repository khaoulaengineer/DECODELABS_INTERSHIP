"""
DecodeLabs — Project 3 : SQL Data Analysis
Auteur : Khaoula
Objectif : Utiliser des requêtes SQL pour extraire des insights du dataset
           e-commerce nettoyé. On charge le fichier dans une base SQLite
           locale (sales.db) pour exécuter de vraies requêtes SQL.

Exigences du brief (Project 3) :
    1. Écrire des requêtes SELECT
    2. Utiliser WHERE, ORDER BY, GROUP BY
    3. Réaliser des agrégations de base (COUNT, SUM, AVG)
    -> Bonus suggéré par DecodeLabs : utiliser HAVING pour filtrer des
       données agrégées, et calculer la contribution en % d'une catégorie.
"""

import sqlite3
import pandas as pd

INPUT_FILE = "Dataset_Cleaned.xlsx"   # dataset nettoyé issu du Project 1
DB_FILE = "sales.db"
TABLE = "orders"

# ----------------------------------------------------------------------
# 0. CHARGEMENT DU DATASET DANS UNE BASE SQLITE
# ----------------------------------------------------------------------
df = pd.read_excel(INPUT_FILE)
conn = sqlite3.connect(DB_FILE)
df.to_sql(TABLE, conn, if_exists="replace", index=False)
print(f"Table '{TABLE}' créée dans {DB_FILE} ({len(df)} lignes)\n")


def run(title, query):
    """Exécute une requête SQL et affiche le résultat."""
    print(f"=== {title} ===")
    print(f"{query.strip()}\n")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    print()
    return result


# ----------------------------------------------------------------------
# 1. SELECT SIMPLE + WHERE
# ----------------------------------------------------------------------
run(
    "1. Commandes livrées avec un montant > 1000",
    """
    SELECT OrderID, Product, TotalPrice, OrderStatus
    FROM orders
    WHERE OrderStatus = 'Delivered' AND TotalPrice > 1000
    ORDER BY TotalPrice DESC
    LIMIT 10;
    """,
)

# ----------------------------------------------------------------------
# 2. GROUP BY + AGGRÉGATIONS (COUNT, SUM, AVG)
# ----------------------------------------------------------------------
run(
    "2. Chiffre d'affaires, nombre de commandes et panier moyen par produit",
    """
    SELECT
        Product,
        COUNT(*)            AS nb_commandes,
        SUM(TotalPrice)      AS chiffre_affaires,
        ROUND(AVG(TotalPrice), 2) AS panier_moyen
    FROM orders
    GROUP BY Product
    ORDER BY chiffre_affaires DESC;
    """,
)

# ----------------------------------------------------------------------
# 3. GROUP BY + ORDER BY sur une méthode de paiement
# ----------------------------------------------------------------------
run(
    "3. Répartition des commandes par méthode de paiement",
    """
    SELECT
        PaymentMethod,
        COUNT(*) AS nb_commandes,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct_du_total
    FROM orders
    GROUP BY PaymentMethod
    ORDER BY nb_commandes DESC;
    """,
)

# ----------------------------------------------------------------------
# 4. HAVING — filtrer sur des données déjà agrégées (bonus DecodeLabs)
# ----------------------------------------------------------------------
run(
    "4. Produits dont le CA dépasse 180 000 (HAVING sur agrégat)",
    """
    SELECT
        Product,
        SUM(TotalPrice) AS chiffre_affaires
    FROM orders
    GROUP BY Product
    HAVING SUM(TotalPrice) > 180000
    ORDER BY chiffre_affaires DESC;
    """,
)

# ----------------------------------------------------------------------
# 5. Analyse temporelle : CA par mois (fonctions de date SQLite)
# ----------------------------------------------------------------------
run(
    "5. Chiffre d'affaires par mois",
    """
    SELECT
        strftime('%Y-%m', Date) AS mois,
        COUNT(*)          AS nb_commandes,
        SUM(TotalPrice)   AS chiffre_affaires
    FROM orders
    GROUP BY mois
    ORDER BY mois;
    """,
)

# ----------------------------------------------------------------------
# 6. WHERE avec condition multiple + ORDER BY (top clients / commandes)
# ----------------------------------------------------------------------
run(
    "6. Top 10 des commandes annulées ou retournées, triées par valeur",
    """
    SELECT OrderID, CustomerID, Product, TotalPrice, OrderStatus
    FROM orders
    WHERE OrderStatus IN ('Cancelled', 'Returned')
    ORDER BY TotalPrice DESC
    LIMIT 10;
    """,
)

conn.close()
print("Analyse SQL terminée. Base disponible dans : sales.db")
