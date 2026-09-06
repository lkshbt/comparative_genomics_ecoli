import pandas as pd

# Load significant family tables
rmci = pd.read_csv(
    "results/RM9387_CI5_Surface_Adhesion_families.csv"
)

c41bl21 = pd.read_csv(
    "results/C41(DE3)_BL21_Carbohydrate_metabolism_families.csv"
)

# Add study information
rmci["pair"] = "RM9387 + CI5"
rmci["enriched_category"] = "Surface/Adhesion"

c41bl21["pair"] = "C41(DE3) + BL21"
c41bl21["enriched_category"] = "Carbohydrate metabolism"

# Combine
summary = pd.concat(
    [rmci, c41bl21],
    ignore_index=True
)

# Keep useful columns first
preferred = [
    "pair",
    "enriched_category",
    "cluster",
    "gene",
    "product",
    "go_function",
    "ontology_term"
]

columns = [c for c in preferred if c in summary.columns]

summary = summary[columns]

# Remove duplicate rows
summary = summary.drop_duplicates()

# Save
output = "results/significant_enriched_gene_families.csv"

summary.to_csv(
    output,
    index=False
)

print("Gene-level summary")
print("=" * 70)

print("\nTotal significant enriched families:", len(summary))

print("\nFamilies by pair:")
print(summary["pair"].value_counts())

print("\nFamilies by functional category:")
print(summary["enriched_category"].value_counts())

print("\nFirst 20 entries:")
print(summary.head(20).to_string(index=False))

print("\nSaved:")
print(output)
