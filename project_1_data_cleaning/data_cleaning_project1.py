"""
DecodeLabs — Project 1 : Data Cleaning & Preparation
Auteur : Khaoula
Objectif : Nettoyer le dataset e-commerce brut (Dataset_for_Data_Analytics.xlsx)
           en traitant les valeurs manquantes, les doublons et les formats
           incorrects, puis produire un dataset "Gold Standard" prêt pour
           l'analyse.

Exigences du brief (Project 1) :
    1. Identifier les valeurs manquantes / nulles
    2. Supprimer les doublons
    3. Corriger les formats (dates, nombres, texte)
    4. Documenter chaque changement (change log) -> traçabilité
    5. Seuil de validation avant Project 2 :
       - 0% de doublons sur les identifiants uniques (OrderID)
       - 0% de dates mal formatées
"""

import pandas as pd

INPUT_FILE = "Dataset_for_Data_Analytics__1_.xlsx"
OUTPUT_FILE = "Dataset_Cleaned.xlsx"
LOG_FILE = "change_log.csv"

change_log = []  # on garde une trace de chaque action -> "If it isn't documented, it didn't happen"


def log_change(change_id, description, impact, status="Resolved"):
    change_log.append(
        {"Change ID": change_id, "Description": description, "Impact": impact, "Status": status}
    )


# ----------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES
# ----------------------------------------------------------------------
df = pd.read_excel(INPUT_FILE)
n_rows_start = len(df)
print(f"Dataset chargé : {n_rows_start} lignes, {df.shape[1]} colonnes\n")


# ----------------------------------------------------------------------
# 2. IDENTIFICATION DES VALEURS MANQUANTES
# ----------------------------------------------------------------------
missing = df.isnull().sum()
missing = missing[missing > 0]
print("Valeurs manquantes détectées par colonne :")
print(missing if not missing.empty else "Aucune valeur manquante détectée.")
print()

# CouponCode : NaN = "pas de code promo utilisé sur cette commande" (pas une erreur,
# mais l'information doit être explicite pour l'analyse -> imputation stratégique,
# pas de suppression de ligne (cf. "Handle the Gaps. Don't just delete.")
n_missing_coupon = df["CouponCode"].isnull().sum()
if n_missing_coupon > 0:
    df["CouponCode"] = df["CouponCode"].fillna("No Coupon")
    log_change(
        "CR001",
        "Imputation de CouponCode manquant par 'No Coupon'",
        f"{n_missing_coupon} lignes concernées, aucune ligne supprimée",
    )


# ----------------------------------------------------------------------
# 3. SUPPRESSION DES DOUBLONS
# ----------------------------------------------------------------------
# a) doublons stricts (ligne entièrement identique)
n_full_dupes = df.duplicated().sum()
if n_full_dupes > 0:
    df = df.drop_duplicates()
    log_change("CR002", "Suppression des lignes strictement dupliquées", f"{n_full_dupes} lignes supprimées")

# b) doublons sur l'identifiant unique OrderID (on garde la 1ère occurrence)
n_id_dupes = df["OrderID"].duplicated().sum()
if n_id_dupes > 0:
    df = df.drop_duplicates(subset="OrderID", keep="first")
    log_change("CR003", "Suppression des doublons sur OrderID", f"{n_id_dupes} lignes supprimées")

print(f"Doublons stricts trouvés : {n_full_dupes}")
print(f"Doublons sur OrderID trouvés : {n_id_dupes}\n")


# ----------------------------------------------------------------------
# 4. CORRECTION DES FORMATS
# ----------------------------------------------------------------------

# --- 4a. Dates -> format ISO 8601 (YYYY-MM-DD) ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
n_bad_dates = df["Date"].isnull().sum()
if n_bad_dates > 0:
    log_change("CR004", "Dates non convertibles détectées", f"{n_bad_dates} lignes à vérifier manuellement", status="Review")
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
log_change("CR005", "Standardisation des dates au format ISO 8601 (YYYY-MM-DD)", f"{n_rows_start} lignes")

# --- 4b. Texte -> trim + casse cohérente (Title Case) ---
text_cols = ["Product", "ShippingAddress", "PaymentMethod", "OrderStatus", "ReferralSource", "CouponCode"]
for col in text_cols:
    before = df[col].copy()
    df[col] = df[col].astype(str).str.strip().str.title()
    n_changed = (before.astype(str) != df[col]).sum()
    if n_changed > 0:
        log_change("CR006", f"Nettoyage texte (trim + title case) sur '{col}'", f"{n_changed} lignes modifiées")

# CustomerID / OrderID / TrackingNumber : identifiants -> majuscules, sans espaces
for col in ["OrderID", "CustomerID", "TrackingNumber"]:
    df[col] = df[col].astype(str).str.strip().str.upper()

# --- 4c. Nombres -> précision à 2 décimales, valeurs cohérentes ---
df["UnitPrice"] = df["UnitPrice"].round(2)
df["TotalPrice"] = df["TotalPrice"].round(2)

# Vérification de cohérence métier : TotalPrice doit être égal à Quantity * UnitPrice
recalculated = (df["Quantity"] * df["UnitPrice"]).round(2)
mismatch_mask = (recalculated - df["TotalPrice"]).abs() > 0.01
n_mismatch = mismatch_mask.sum()
if n_mismatch > 0:
    df.loc[mismatch_mask, "TotalPrice"] = recalculated[mismatch_mask]
    log_change("CR007", "Recalcul de TotalPrice incohérent (Quantity x UnitPrice)", f"{n_mismatch} lignes corrigées")
else:
    log_change("CR007", "Contrôle de cohérence TotalPrice = Quantity x UnitPrice", "0 incohérence trouvée")

log_change("CR008", "Arrondi de UnitPrice et TotalPrice à 2 décimales", f"{n_rows_start} lignes")


# ----------------------------------------------------------------------
# 5. VALIDATION FINALE (seuil de passage vers Project 2)
# ----------------------------------------------------------------------
final_id_dupes = df["OrderID"].duplicated().sum()
final_bad_dates = df["Date"].apply(
    lambda x: pd.to_datetime(x, format="%Y-%m-%d", errors="coerce")
).isnull().sum()

print("=== VALIDATION ===")
print(f"Doublons OrderID restants : {final_id_dupes} (objectif : 0)")
print(f"Dates mal formatées restantes : {final_bad_dates} (objectif : 0)")
assert final_id_dupes == 0, "Echec : des doublons OrderID subsistent."
assert final_bad_dates == 0, "Echec : des dates mal formatées subsistent."
print("Validation réussie : dataset conforme au seuil du Project 2.\n")


# ----------------------------------------------------------------------
# 6. EXPORT
# ----------------------------------------------------------------------
df.to_excel(OUTPUT_FILE, index=False)
pd.DataFrame(change_log).to_csv(LOG_FILE, index=False)

print(f"Dataset nettoyé exporté vers : {OUTPUT_FILE} ({len(df)} lignes)")
print(f"Change log exporté vers : {LOG_FILE}")
