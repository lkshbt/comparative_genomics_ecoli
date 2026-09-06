import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

# -----------------------------
# Input files
# -----------------------------
presence = pd.read_csv(
    "results/family_presence_absence.csv",
    index_col="family"
)

annotations = pd.read_csv(
    "results/functional_analysis.csv"
)

# -----------------------------
# Define strain pairs
# -----------------------------
rmci = ["GCF_000801165.1", "GCF_000971615.1"]
c41bl21 = ["GCF_000830035.1", "GCF_000833145.1"]

# -----------------------------
# Identify pair-specific families
# -----------------------------
def get_pair_specific(pair):
    other = [c for c in presence.columns if c not in pair]

    mask = (
        (presence[pair[0]] == 1) &
        (presence[pair[1]] == 1) &
        (presence[other].sum(axis=1) == 0)
    )

    return set(presence.index[mask])


rmci_families = get_pair_specific(rmci)
c41bl21_families = get_pair_specific(c41bl21)

print("RM9387 + CI5 pair-specific families:", len(rmci_families))
print("C41(DE3) + BL21 pair-specific families:", len(c41bl21_families))

# -----------------------------
# Functional categories
# -----------------------------
keywords = {
    "Mobile elements/Recombination": [
        "recombinase", "integrase", "transpos", "phage",
        "prophage", "retro", "mobile element"
    ],

    "Regulation": [
        "transcriptional regulator", "transcription factor",
        "repressor", "activator", "DNA-binding"
    ],

    "DNA defense/Repair": [
        "endonuclease", "exonuclease", "restriction",
        "recA", "recB", "recC", "recE", "repair",
        "toxin", "antitoxin", "defense"
    ],

    "Surface/Adhesion": [
        "fimbr", "pilus", "adhes", "outer membrane",
        "secretion", "tss", "O-antigen"
    ],

    "Carbohydrate metabolism": [
        "sugar", "carbohydrate", "glycosyl",
        "polymerase", "acetyltransferase"
    ],

    "Transport": [
        "transporter", "permease", "transport",
        "ABC", "binding protein"
    ]
}

# -----------------------------
# Prepare annotation table
# -----------------------------
ann = annotations.copy()

ann["family"] = ann["cluster"]

ann["product_clean"] = (
    ann["product"]
    .fillna("")
    .astype(str)
    .str.lower()
)

# One representative annotation per family
family_ann = (
    ann.sort_values("product_clean")
       .drop_duplicates("family")
       [["family", "product_clean"]]
)

family_ann["category"] = "Hypothetical/Unknown"

for category, terms in keywords.items():
    pattern = "|".join(terms)

    mask = family_ann["product_clean"].str.contains(
        pattern,
        regex=True,
        na=False
    )

    family_ann.loc[mask, "category"] = category

# -----------------------------
# Enrichment function
# -----------------------------
def enrichment(target_families, label):

    target = family_ann["family"].isin(target_families)

    results = []

    for category in sorted(family_ann["category"].unique()):

        category_mask = family_ann["category"] == category

        a = (target & category_mask).sum()
        b = (target & ~category_mask).sum()
        c = (~target & category_mask).sum()
        d = (~target & ~category_mask).sum()

        table = [
            [a, b],
            [c, d]
        ]

        odds_ratio, pvalue = fisher_exact(
            table,
            alternative="greater"
        )

        results.append({
            "pair": label,
            "category": category,
            "target_families": int(a),
            "target_total": int(target.sum()),
            "background_families": int(c),
            "background_total": int((~target).sum()),
            "odds_ratio": odds_ratio,
            "p_value": pvalue
        })

    result = pd.DataFrame(results)

    # FDR correction
    result["FDR"] = multipletests(
        result["p_value"],
        method="fdr_bh"
    )[1]

    result["significant_FDR_0.05"] = (
        result["FDR"] < 0.05
    )

    return result


# -----------------------------
# Run enrichment
# -----------------------------
rmci_result = enrichment(
    rmci_families,
    "RM9387 + CI5"
)

c41_result = enrichment(
    c41bl21_families,
    "C41(DE3) + BL21"
)

final = pd.concat(
    [rmci_result, c41_result],
    ignore_index=True
)

# -----------------------------
# Save results
# -----------------------------
output = "results/pair_functional_enrichment.csv"

final.to_csv(
    output,
    index=False
)

print("\nFunctional enrichment results:")
print(
    final[
        [
            "pair",
            "category",
            "target_families",
            "odds_ratio",
            "p_value",
            "FDR",
            "significant_FDR_0.05"
        ]
    ].to_string(index=False)
)

print("\nSaved:")
print(output)
