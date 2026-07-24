"""
DecodeLabs — Project 2 : Exploratory Data Analysis (EDA)
Auteur : Khaoula
Objectif : Analyser le dataset e-commerce nettoyé (Dataset_Cleaned.xlsx, issu du
           Project 1) pour comprendre les tendances, distributions et anomalies.

Exigences du brief (Project 2) :
    1. Calculer des statistiques de base (mean, median, count)
    2. Identifier les tendances et les valeurs aberrantes (outliers)
    3. Résumer les observations clés
    -> Bonus suggéré par DecodeLabs : explorer les corrélations entre
       variables et visualiser les distributions.
"""

import pandas as pd
import numpy as np

INPUT_FILE = "Dataset_Cleaned.xlsx"   # dataset nettoyé issu du Project 1

df = pd.read_excel(INPUT_FILE)
print(f"Dataset chargé : {len(df)} lignes, {df.shape[1]} colonnes\n")


# ----------------------------------------------------------------------
# 1. STATISTIQUES DE BASE (mean, median, count)
# ----------------------------------------------------------------------
numeric_cols = ["Quantity", "UnitPrice", "TotalPrice", "ItemsInCart"]

print("=== STATISTIQUES DESCRIPTIVES ===")
stats = df[numeric_cols].agg(["count", "mean", "median", "std", "min", "max"]).round(2)
print(stats, "\n")

# Comptages sur les variables catégorielles
print("=== RÉPARTITION PAR CATÉGORIE ===")
for col in ["Product", "PaymentMethod", "OrderStatus"]:
    print(f"\n-- {col} --")
    print(df[col].value_counts())
print()


# ----------------------------------------------------------------------
# 2. IDENTIFICATION DES TENDANCES
# ----------------------------------------------------------------------
# a) Evolution des ventes dans le temps (par mois)
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")
monthly_sales = df.groupby("Month")["TotalPrice"].sum().round(2)
print("=== TENDANCE : CHIFFRE D'AFFAIRES PAR MOIS ===")
print(monthly_sales, "\n")

# b) Produit le plus vendu (en quantité et en CA)
top_products_qty = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
top_products_rev = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False).round(2)
print("=== TOP PRODUITS (Quantité) ===")
print(top_products_qty, "\n")
print("=== TOP PRODUITS (Chiffre d'affaires) ===")
print(top_products_rev, "\n")

# c) Méthode de paiement dominante
payment_share = (df["PaymentMethod"].value_counts(normalize=True) * 100).round(1)
print("=== RÉPARTITION DES MÉTHODES DE PAIEMENT (%) ===")
print(payment_share, "\n")


# ----------------------------------------------------------------------
# 3. DÉTECTION DES OUTLIERS (méthode IQR — robuste pour les données business)
# ----------------------------------------------------------------------
def detect_outliers_iqr(series, factor=1.5):
    """Retourne les valeurs aberrantes selon la méthode de l'IQR (boxplot)."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return series[(series < lower) | (series > upper)], lower, upper

print("=== DÉTECTION DES OUTLIERS (IQR) ===")
for col in numeric_cols:
    outliers, lower, upper = detect_outliers_iqr(df[col])
    print(f"{col}: {len(outliers)} outliers détectés "
          f"(bornes attendues : [{lower:.2f} ; {upper:.2f}])")
print()


# ----------------------------------------------------------------------
# 4. ANALYSE DE CORRÉLATION (bonus)
# ----------------------------------------------------------------------
print("=== MATRICE DE CORRÉLATION (variables numériques) ===")
corr_matrix = df[numeric_cols].corr(numeric_only=True).round(2)
print(corr_matrix, "\n")


# ----------------------------------------------------------------------
# 5. RÉSUMÉ DES OBSERVATIONS CLÉS ("So What?")
# ----------------------------------------------------------------------
n_orders = len(df)
total_revenue = df["TotalPrice"].sum()
avg_order_value = df["TotalPrice"].mean()
best_product = top_products_rev.index[0]
best_month = monthly_sales.idxmax()
top_payment = payment_share.index[0]

summary = f"""
=== RÉSUMÉ EXÉCUTIF ===
- {n_orders} commandes analysées, pour un chiffre d'affaires total de {total_revenue:,.2f}.
- Panier moyen (Average Order Value) : {avg_order_value:.2f}.
- Le produit générant le plus de revenu est : {best_product}.
- Le mois avec le plus fort chiffre d'affaires est : {best_month}.
- La méthode de paiement la plus utilisée est : {top_payment} ({payment_share.iloc[0]}% des commandes).
- Des outliers ont été détectés sur {', '.join([c for c in numeric_cols if len(detect_outliers_iqr(df[c])[0]) > 0])} 
  -> à investiguer : anomalies de saisie ou véritables clients/commandes exceptionnelles.
"""
print(summary)

with open("eda_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print("Résumé exécutif exporté vers : eda_summary.txt")
